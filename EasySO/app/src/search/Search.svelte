<script>
  import SearchInput from "./SearchInput.svelte";
  import ResultsBar from "../Common/ResultsBar.svelte";
  import SearchItem from "./SearchItem.svelte";
  import SearchNoResults from "./SearchNoResults.svelte";
  import Loader from "../common/Loader.svelte";
  import Tag from "../tag/tag.svelte";

  export let searchData;
  export let totalResults;
  export let tagData;
  export let isLoading;
  export let initialInstruction;
  export let errorObj;
  export let PyStackBotResults;
  let relatedQuestions = null;

</script>

<style>
  .tag-loader {
    margin-top: 20px;
  }
</style>

<SearchInput {tagData} {isLoading} {initialInstruction} {errorObj} on:searchInput on:searchByTag />

{#if !initialInstruction}
  {#if tagData === null}
    <ResultsBar {isLoading} {relatedQuestions} />
    {#if isLoading }
    <Loader />
    {/if}

    {#if searchData && totalResults !== 0}
    <SearchItem {isLoading} {searchData} on:gotoQuestion on:searchByTag />
    {:else if !isLoading}
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