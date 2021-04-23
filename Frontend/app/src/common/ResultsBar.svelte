<script>
  import QuestionsRelated from "../question/QuestionsRelated.svelte";
  export let results;
  export let isLoading;
  export let relatedQuestions;
  let showRelatedQuestions;

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
</style>

<section>

  <div>
    <h2>
      Top Results
      <!-- {#if results > 0}
        {total} {title}
      {:else if results === 0}{titleForNoResults}{:else if isLoading}&nbsp;{/if} -->
    </h2>

  </div>
  {#if relatedQuestions}
    <div class="link link-questions">
      {#if !showRelatedQuestions}
        view related questions
      {:else}hide related questions{/if}
    </div>
  {/if}

</section>

{#if relatedQuestions}
  <QuestionsRelated
      {relatedQuestions}
      on:closeRelatedQuestions={toggleRelatedQuestions}
      on:relatedQuestionSearch
  />
{/if}