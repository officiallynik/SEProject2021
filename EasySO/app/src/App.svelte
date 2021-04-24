<script>
  import { section, searchQuery } from "./stores/common.js";
  import { vscodeProgress } from "./stores/vscode-api.js";
  import { selectedSearchFilter } from "./stores/results-filter.js";
  import axios from "axios";
  import Header from "./common/Header.svelte";
  import Question from "./question/Question.svelte";
  import Search from "./search/Search.svelte";

  let searchData;
  let questionId;
  let questionTitle;
  let totalResults;
  let isLoading = false;
  let extensionAction;
  let selectedTag;
  let tagData;
  let initialInstruction = true;
  let errorObj;
  let PyStackBotAnswers;
  let PyStackBotSummary;
  let PyStackBotRelatedQuestions;

  window.addEventListener("message", (event) => {
    extensionAction = event.data.action;

    if (event.data.action === "search") {
      searchQuery.set(event.data.query);
      selectedSearchFilter.set("Relevance");
      searchPyStackBot();
      section.set("search");
    }

    if (event.data.action === "searchError") {
      searchQuery.set(event.data.query.error);
      selectedSearchFilter.set("Relevance");
      searchSO();
      section.set("search");
      errorObj = event.data.query;
    }
  });

  function handleGotoQuestion(event) {
    section.set("question");
    questionId = event.detail.questionId;
    questionTitle = event.detail.questionTitle;
  }

  function handleGotoSearch(event) {
    section.set("search");
  }

  function handlePageSearch() {}

  function handleFilterChangeSearch() {}

  function handleTagFromQuestionSearch(event) {
    handleTagSelected(event);
  }

  function handleTechnicalQuery(query) {
  
    vscodeProgress("start", "Searching PyStackBot", false);
    isLoading = true;
    tagData = null;
    selectedTag = null;
    errorObj = null;
    searchData = null;
    PyStackBotAnswers = null;

    const uri = `http://localhost:5000/search/summary?query=${query}`;
    console.log("pystackbot search....");
    axios
      .get(uri)
      .then((response) => {
        isLoading = false;

        if (response.status === 200) {
          console.log("got response...");
          PyStackBotRelatedQuestions = response.data.questions;
          PyStackBotSummary = response.data.answers;
          vscodeProgress("stop", null, false);
        } else {
          vscodeProgress("stop", null, true);
        }
      })
      .catch(() => {
        isLoading = false;
        vscodeProgress("stop", null, true);
      });
  }

  // Search by selected tag - Only gets the wiki info
  function handleTagSelected(event) {
    vscodeProgress("start", "Loading Tag Results", false);
    isLoading = true;
    window.scroll({ top: 0, behavior: "smooth" });
    selectedTag = event.detail.tag;

    const uri = `https://api.stackexchange.com/2.2/tags/${selectedTag}/wikis?site=stackoverflow&filter=!9_bDDrGXY`;

    console.log("TagSearch req...");
    axios
      .get(uri)
      .then((response) => {
        if (response.status === 200) {
          tagData = response.data.items[0];
          // section.set("tag");
        }
        if (tagData === undefined) {
          tagData = {
            tag_name: selectedTag,
            error_msg: "No wiki found for given tag :(",
          };
        }
      })
      .catch(() => {})
      .finally(() => {
        isLoading = false;
        vscodeProgress("stop", null, true);
        addCopyOption();
      });
  }

  // stackoverflow direct search functionality
  function searchSO() {
    if ($searchQuery.length !== 0) {
      initialInstruction = false;
    }

    if (
      $searchQuery[0] === "[" &&
      $searchQuery[$searchQuery.length - 1] === "]"
    ) {
      let split = $searchQuery.substring(1, $searchQuery.length - 1).split(" ");
      if (split.length === 1) {
        const tag = $searchQuery.substring(1, $searchQuery.length - 1);
        handleTagSelected({ detail: { tag: tag } });
        errorObj = null;
        return;
      } else {
        const techQuery = $searchQuery.substring(1, $searchQuery.length - 1);
        handleTechnicalQuery(techQuery);
        errorObj = null;
        return;
      }
    }

    tagData = null;
    selectedTag = null;
    errorObj = null;
    PyStackBotRelatedQuestions = null;
    PyStackBotAnswers = null;
    PyStackBotSummary = null;

    if ($searchQuery.length > 0) {
      vscodeProgress("start", "Loading Search Results", false);
      isLoading = true;

      const uri = `https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=relevance&q=${$searchQuery}&site=stackoverflow&filter=withbody`;
      console.log("query search...");
      axios
        .get(uri)
        .then((response) => {
          isLoading = false;
          console.log(response.data);
          if (response.status === 200) {
            searchData = response.data.items;
            totalResults = searchData.length;
            vscodeProgress("stop", null, false);
          } else {
            vscodeProgress("stop", null, true);
          }
        })
        .catch(() => {
          isLoading = false;
          vscodeProgress("stop", null, true);
        });
    }
  }

  // stackoverflow direct search functionality
  function searchPyStackBot() {
    console.log("query", $searchQuery);

    if ($searchQuery.length !== 0) {
      initialInstruction = false;
    }

    if (
      $searchQuery[0] === "[" &&
      $searchQuery[$searchQuery.length - 1] === "]"
    ) {
      let split = $searchQuery.substring(1, $searchQuery.length - 1).split(" ");
      if (split.length === 1) {
        const tag = $searchQuery.substring(1, $searchQuery.length - 1);
        handleTagSelected({ detail: { tag: tag } });
        errorObj = null;
        return;
      } else {
        const techQuery = $searchQuery.substring(1, $searchQuery.length - 1);
        handleTechnicalQuery(techQuery);
        errorObj = null;
        return;
      }
    }

    tagData = null;
    selectedTag = null;
    errorObj = null;
    searchData = null;
    PyStackBotSummary = null;

    if ($searchQuery.length > 0) {
      vscodeProgress("start", "Searching PyStackBot", false);
      isLoading = true;

      const uri = `http://localhost:5000/search?query=${$searchQuery}`;
      console.log("pystackbot search....");
      axios
        .get(uri)
        .then((response) => {
          isLoading = false;

          if (response.status === 200) {
            console.log("got response...");
            PyStackBotRelatedQuestions = response.data.questions;
            PyStackBotAnswers = response.data.answers;
            vscodeProgress("stop", null, false);
          } else {
            vscodeProgress("stop", null, true);
          }
        })
        .catch(() => {
          isLoading = false;
          vscodeProgress("stop", null, true);
        });
    }
  }
</script>

<Header on:goBack={handleGotoSearch} {extensionAction} />

{#if $section === "search"}
  <Search
    on:gotoQuestion={handleGotoQuestion}
    on:gotoTagLearnMore={() => section.set("tag")}
    on:searchByTag={handleTagSelected}
    on:searchSO={searchSO}
    on:searchPyStackBot={searchPyStackBot}
    on:searchByPage={handlePageSearch}
    on:filterChange={handleFilterChangeSearch}
    {isLoading}
    {searchData}
    {tagData}
    {totalResults}
    {initialInstruction}
    {errorObj}
    {PyStackBotAnswers}
    {PyStackBotRelatedQuestions}
    {PyStackBotSummary}
  />
{:else if $section === "question"}
  <Question
    on:searchByTag={handleTagFromQuestionSearch}
    {questionId}
    {questionTitle}
    {extensionAction}
  />
{/if}
