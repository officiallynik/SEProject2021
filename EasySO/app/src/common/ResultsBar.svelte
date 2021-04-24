<script>
  import { createEventDispatcher } from "svelte";
  import QuestionsRelated from "../question/QuestionsRelated.svelte";
  export let results;
  export let isLoading;
  export let PyStackBotRelatedQuestions;
  let showRelatedQuestions = false;
  let relatedQuestions = null;

  function toggleRelatedQuestions() {
    showRelatedQuestions = !showRelatedQuestions;
  }

  const dispatch = createEventDispatcher();
  function handleGotoQuestion(event) {
    console.log("rq", event.detail.questionId, event.detail.questionTitle);
    if (!isLoading) {
      dispatch("gotoQuestion", {
        questionId: event.detail.questionId,
        questionTitle: event.detail.questionTitle
      });
    }
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
      {#if PyStackBotRelatedQuestions}
        PyStackBot Results
      {:else if isLoading}
        Loading...
      {:else}
        Stack Overflow Results
      {/if}
    </h2>

  </div>
  {#if PyStackBotRelatedQuestions}
    <div class="link link-questions" on:click={toggleRelatedQuestions}>
      {#if !showRelatedQuestions}
        view related questions
      {:else}hide related questions{/if}
    </div>
  {/if}

</section>

{#if PyStackBotRelatedQuestions && showRelatedQuestions}
  <QuestionsRelated
      {PyStackBotRelatedQuestions}
      {relatedQuestions}
      on:closeRelatedQuestions={toggleRelatedQuestions}
      on:relatedQuestionSearch={handleGotoQuestion}
  />
{/if}