<script>
  import { fade } from "svelte/transition";
  import { formatNumber } from "../stores/common.js";
  import QuestionsRelated from "./QuestionsRelated.svelte";

  export let title;
  export let creationDate;
  export let lastActivityDate;
  export let viewCount;
  export let extensionAction;
  export let relatedQuestions;
  let PyStackBotRelatedQuestions = null;
  let showRelatedQuestions;

  $: totalViews = formatNumber(viewCount);

  function toggleRelatedQuestions() {
    showRelatedQuestions = !showRelatedQuestions;
  }
</script>

<h1>
  {@html title}
</h1>

<div class="question-title-container" in:fade>
  <div class="metrics">
    {#if creationDate}
      asked
      <span>{new Date(creationDate*1000).toDateString()}</span>
    {/if}

    {#if totalViews}
      views
      <span>{totalViews}</span>
    {/if}

    <span
      class="link view-related-questions"
      class:hide-related-questions={showRelatedQuestions}
      on:click={toggleRelatedQuestions}
    >
      {#if !showRelatedQuestions}
        view related questions
      {:else}hide related questions{/if}
    </span>

    {#if showRelatedQuestions}
      <QuestionsRelated
        {relatedQuestions}
        {PyStackBotRelatedQuestions}
        on:closeRelatedQuestions={toggleRelatedQuestions}
        on:relatedQuestionSearch
      />
    {/if}
  </div>
</div>

<style>
  .question-title-container {
    border-bottom: 2px solid var(--vscode-textSeparator-foreground);
    padding: 6px 0;
  }
  h1 {
    margin: 6px 0;
    word-break: break-word;
  }
  .metrics {
    margin-top: 10px;
    height: 22px;
  }
  .metrics span:not(:last-of-type) {
    margin-right: 20px;
    font-weight: bold;
  }
  .metrics span.view-related-questions,
  .metrics span.hide-related-questions {
    float: right;
  }
  .view-related-questions {
    color: var(--vscode-textLink-activeForeground);
    opacity: 0.8;
  }
  .view-related-questions:hover {
    opacity: 1;
  }
  .hide-related-questions {
    color: var(--vscode-textLink-activeForeground);
    opacity: 0.8;
  }
  .hide-related-questions:hover {
    opacity: 1;
  }
</style>
