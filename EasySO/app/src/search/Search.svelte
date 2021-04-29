<!--
  search section svelte file
-->

<script>
  import SearchInput from "./SearchInput.svelte";
  import ResultsBar from "../Common/ResultsBar.svelte";
  import SearchItem from "./SearchItem.svelte";
  import SearchNoResults from "./SearchNoResults.svelte";
  import Loader from "../common/Loader.svelte";
  import Tag from "../tag/tag.svelte";
  import QuestionAnswers from "../question/QuestionAnswers.svelte";

  export let searchData;
  export let totalResults;
  export let tagData;
  export let isLoading;
  export let initialInstruction;
  export let errorObj;
  export let PyStackBotAnswers;
  export let PyStackBotSummary;
  export let PyStackBotRelatedQuestions;

</script>

<style>
  .tag-loader {
    margin-top: 20px;
  }
</style>

<!-- search input box -->
<SearchInput {tagData} {isLoading} {initialInstruction} {errorObj} on:searchSO on:searchPyStackBot on:searchByTag />

<!-- instruction box, search items -->
{#if !initialInstruction}
  {#if tagData === null}
    <ResultsBar {isLoading} {PyStackBotRelatedQuestions} {PyStackBotSummary} on:gotoQuestion />
    {#if isLoading }
    <Loader />
    {/if}

    {#if searchData && totalResults !== 0}
      <SearchItem {isLoading} {searchData} on:gotoQuestion on:searchByTag />
    {:else if !isLoading && PyStackBotSummary && PyStackBotAnswers}
      <SearchNoResults />
    {/if}
  {:else}
    {#if isLoading }
      <div class="tag-loader">
        <Loader />
      </div>
    {/if}
    <Tag {tagData} />
  {/if}
{/if}

<!-- pystackbot answers display -->
{#if PyStackBotAnswers}
  <QuestionAnswers 
    {PyStackBotAnswers}
  />
{/if}

<!-- pystackbot summarised answer display -->
{#if PyStackBotSummary}
  {#each PyStackBotSummary as answer}
    {@html answer}
  {/each}
{/if}