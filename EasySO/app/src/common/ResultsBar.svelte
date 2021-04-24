<script>
  import QuestionsRelated from "../question/QuestionsRelated.svelte";
  export let results;
  export let isLoading;
  export let relatedQuestions;
  let showRelatedQuestions = false;

  function toggleRelatedQuestions() {
    showRelatedQuestions = !showRelatedQuestions;
  }
</script>

<style>
  section {
    border-bottom: 2px solid var(--vscode-textSeparator-foreground);
    display: flex;
    align-items: center;
  }
  div:first-of-type {
    width: 30%;
  }
  div:last-of-type {
    width: 70%;
    text-align: right;
  }
  .link-questions {
    color: var(--vscode-textLink-foreground);
    user-select: none;
    opacity: 0.8;
  }
  .link-questions:hover {
    opacity: 1;
  }
  .results-header {
    float: left;
  }
</style>

<section>

  <div>
    <h2 class="results-header">
      {#if relatedQuestions}
        PyStackBot Results
      {:else if isLoading}
        Loading...
      {:else}
        Stack Overflow Results
      {/if}
    </h2>

  </div>
  {#if relatedQuestions}
    <div class="link link-questions" on:click={toggleRelatedQuestions}>
      {#if !showRelatedQuestions}
        view related questions
      {:else}hide related questions{/if}
    </div>
  {/if}

</section>

{#if relatedQuestions && showRelatedQuestions}
  <QuestionsRelated
      {relatedQuestions}
      on:closeRelatedQuestions={toggleRelatedQuestions}
      on:relatedQuestionSearch
  />
{/if}