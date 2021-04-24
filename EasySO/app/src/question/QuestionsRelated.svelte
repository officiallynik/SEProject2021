<script>
  import { createEventDispatcher } from "svelte";
  import { fade } from "svelte/transition";

  export let relatedQuestions;

  console.log("RQS", relatedQuestions[0].question.title, relatedQuestions[1].question.title);

  const dispatch = createEventDispatcher();
  function gotoRelatedQuestion(questionId, questionTitle) {
    dispatch("relatedQuestionSearch", {
      questionId: questionId,
      questionTitle: questionTitle
    });
    dispatch("closeRelatedQuestions");
  }
</script>

<style>
  section {
    margin-top: 26px;
    border-bottom: 2px solid var(--vscode-textSeparator-foreground);
  }
  header {
    float: left;
    font-size: 11px;
    min-width: 40px;
    text-align: center;
    margin-right: 16px;
    padding: 1px 4px;
    font-weight: bold;
  }
  .is-answered,
  .has-answer {
    border-radius: 2px;
  }
  .is-answered {
    background-color: var(--vscode-textLink-foreground);
    color: var(--vscode-badge-foreground);
  }
  .has-answer {
    border: 1px solid var(--vscode-textLink-foreground);
  }
  p {
    font-size: 13px;
  }
</style>

<section in:fade>
  {#each relatedQuestions as question}
    {#if question.score && question.is_answered && question.answer_count}
      <header
        class:is-answered={question.is_answered}
        class:has-answer={question.answer_count}>
        {question.score}
      </header>
    {/if}
    {#if question.question_id && question.title}
      <p
        class="link"
        on:click={() => gotoRelatedQuestion(question.question_id, question.title)}>
        {@html question.title}
      </p>
    {/if}
    {#if question.question}
      <header
        class:is-answered={true}
        class:has-answer={true}>
        {question.score.toFixed(2)}
      </header>
      <p
        class="link"
        on:click={() => gotoRelatedQuestion(question.question.id, question.question.title)}>
        {@html question.question.title}
      </p>
    {/if}
  {/each}
</section>
