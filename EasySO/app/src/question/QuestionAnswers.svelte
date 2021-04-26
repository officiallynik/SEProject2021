<!--
  answer display svelte file, for given question
-->
<script>
  import Comments from "../common/Comments.svelte";
  import RowLayout from "../common/RowLayout.svelte";
  import ResultsBar from "../Common/ResultsBar.svelte";
  import Loader from "../Common/Loader.svelte";
  import User from "../Common/User.svelte";
  import Tags from "../Common/Tags.svelte";
  import QuestionAnswerIndicies from "./QuestionAnswerIndicies.svelte";

  export let questionId;
  export let answers;
  export let PyStackBotAnswers;
  export let isAnswersLoading;
</script>

<style>
  section {
    border-bottom: 2px solid var(--vscode-textSeparator-foreground);
  }
  section:last-of-type {
    border-bottom: 0;
  }
  /* Duplicate styles from Questions.svelte */
  .question-answer-bottom {
    display: block;
    width: 100%;
    height: 82px;
  }
</style>

<!-- result bar display -->
{#if !PyStackBotAnswers}
  <ResultsBar
    {isAnswersLoading}
  />
{/if}

<!-- loader -->
{#if isAnswersLoading}
  <Loader />
{/if}

<!-- SO answers -->
{#if answers}
  {#each answers as answer, i}
    <section>
      <RowLayout>

        <div slot="left">
          <QuestionAnswerIndicies
            score={answer.score}
            isAccepted={answer.is_accepted} />
        </div>

        <div slot="right">
          <div>
            {@html answer.body}
          </div>

          {#if answer.tags}
            <Tags tags={answer.tags} />
          {/if}

          <div class="question-answer-bottom">
            <User user={answer.owner} createdDate={answer.creation_date} />
          </div>

          {#if answer.comments}
            <Comments comments={answer.comments} />
          {/if}
        </div>
      </RowLayout>
    </section>
  {/each}
{/if}

<!-- pystackbot answers -->
{#if PyStackBotAnswers}
  {#each PyStackBotAnswers as answer, i}
    <section>
      <RowLayout>

        <div slot="left">
          <QuestionAnswerIndicies
            score={answer.score}
            isAccepted={false} />
        </div>

        <div slot="right">
          <div>
            {@html answer.body}
          </div>
        </div>
      </RowLayout>
    </section>
  {/each}
{/if}