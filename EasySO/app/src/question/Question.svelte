<!--
  individual question display given id and title
-->
<script>
  import { onMount } from "svelte";
  import { vscodeProgress } from "../stores/vscode-api.js";
  import axios from "axios";
  import Comments from "../Common/Comments.svelte";
  import RowLayout from "../Common/RowLayout.svelte";
  import User from "../Common/User.svelte";
  import Tags from "../Common/Tags.svelte";
  import Loader from "../Common/Loader.svelte";
  import QuestionTitle from "./QuestionTitle.svelte";
  import QuestionAnswers from "./QuestionAnswers.svelte";
  import QuestionIndices from "./QuestionIndices.svelte";

  export let questionId;
  export let questionTitle;
  export let gif;
  export let extensionAction;
  export let isAnswersLoading;
  export let answers;
  let question;
  let isLoading = true;
  let relatedQuestions;

  // call fetchquestions with id and title on mount
  onMount(() => {
    fetchQuestion();
  });

  // refresh question page on related question click
  function handleOnRelatedSearch(event) {
    isLoading = true;
    questionId = event.detail.questionId;
    questionTitle = event.detail.questionTitle;
    fetchQuestion();
  }

  // fetch related questions related to current question
  function fetchRelatedQuestions() {
    isLoading = true;

    const site = `stackoverflow`;
    const uri = `https://api.stackexchange.com/2.2/questions/${questionId}/related?order=desc&sort=activity&site=${site}`;

    console.log("fetchRelatedQuestions req...");
    axios.get(uri).then((response) => {
      isLoading = false;
      if (response.status === 200) {
        relatedQuestions = response.data.items;
        vscodeProgress("stop", null, false);
      } else {
        vscodeProgress("stop", null, true);
      }
    });
  }

  // fetch full question info with given id
  function fetchQuestion() {
    vscodeProgress("start", "Loading Search Results", false);
    const site = `stackoverflow`;
    const uri = `https://api.stackexchange.com/2.2/questions/${questionId}?site=${site}&filter=!3zl2.5epWZZhmbtbF`;

    console.log("fetchQuestions req...");
    axios.get(uri).then((response) => {
      isLoading = false;
      
      if (response.status === 200) {
        question = response.data.items[0];
        fetchRelatedQuestions();
        fetchAnswers();
      } else {
        vscodeProgress("stop", null, true);
      }
    });
  }

  // fetch all answers of the current question
  function fetchAnswers() {
    const uri = `https://api.stackexchange.com/2.2/questions/${questionId}/answers?order=desc&sort=votes&site=stackoverflow&filter=!3zl2.GhG14q1O7U25`;

    console.log("fetchAnswers req...");
    axios.get(uri).then(response => {
      isLoading = false;
      if (response.status === 200) {
        answers = response.data.items;
      } else {
        vscodeProgress("stop", null, true);
      }
    });
  }
</script>

<QuestionTitle
  on:relatedQuestionSearch={handleOnRelatedSearch}
  title={questionTitle}
  creationDate={question && question.creation_date}
  viewCount={question && question.view_count}
  {relatedQuestions}
  {extensionAction}
/>

{#if isLoading}
  <Loader />
{/if}

{#if question}
  <RowLayout>
    <div slot="left">
      <QuestionIndices
        score={question.score}
        favorite={question.favorite_count}
      />
    </div>

    <div slot="right">
      <div class="content">
        {@html question.body}
      </div>

      <div class="tags">
        <Tags tags={question.tags} on:searchByTag />
      </div>

      <div class="question-answer-bottom">
        <!-- <div class="view-online">
          <a href={question.link} target="_blank">view online</a>
        </div> -->

        <User
          user={question.owner}
          createdDate={question.creation_date}
          isQuestion={true}
        />
      </div>

      {#if question.comments}
        <Comments comments={question.comments} />
      {/if}
    </div>
  </RowLayout>

  {#if question.answer_count > 0}
    <QuestionAnswers {answers} />
  {/if}
{/if}

<style>
  .content {
    min-height: 90px;
  }
  .tags {
    margin-top: 20px;
  }
  .question-answer-bottom {
    display: block;
    width: 100%;
    height: 70px;
    margin-bottom: 30px;
  }
  .view-online {
    width: 100%;
    align-self: center;
  }
  .view-online a {
    cursor: pointer;
    float: left;
    margin-top: 38px;
  }
</style>
