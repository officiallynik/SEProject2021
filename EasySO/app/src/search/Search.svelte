<!--
  search section svelte file
-->

<script>
  import { afterUpdate } from "svelte";
  import SearchInput from "./SearchInput.svelte";
  import ResultsBar from "../Common/ResultsBar.svelte";
  import SearchItem from "./SearchItem.svelte";
  import SearchNoResults from "./SearchNoResults.svelte";
  import Loader from "../common/Loader.svelte";
  import Tag from "../tag/tag.svelte";
  import QuestionAnswers from "../question/QuestionAnswers.svelte";
  import createCopyBtn from '../stores/copy-btn';

  export let searchData;
  export let totalResults;
  export let tagData;
  export let isLoading;
  export let initialInstruction;
  export let errorObj;
  export let PyStackBotAnswers;
  export let PyStackBotSummary;
  export let PyStackBotRelatedQuestions;

  /** 
   * add copy to clipboard buttons to code section after getting answers
  */
  afterUpdate(() => {
    if(PyStackBotSummary || PyStackBotAnswers){
      // remove existing copy btns
      let copy_btns = document.getElementsByClassName('copy-btn');
      for(let i=0; i<copy_btns.length; i++){
        copy_btns[i].remove();
      }

      // add copy btns to codes
      let codeElements = document.getElementsByTagName('pre'); 
      for(let i=0; i<codeElements.length; i++){
        codeElements[i].firstElementChild.id = `code-ele-${i}`;
        const copyBtn = createCopyBtn(`copy-btn-${i}`);
        copyBtn.onclick = () => {
          let copyText = document.getElementById(`code-ele-${i}`).innerText;
          navigator.clipboard.writeText(copyText);
        }
        codeElements[i].prepend(copyBtn);
      }
    }
  });

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