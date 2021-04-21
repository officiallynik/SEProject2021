<script>
  import { section, searchQuery } from "./stores/common.js";
  import { vscodeProgress } from "./stores/vscode-api.js";
  import {
    selectedSearchFilter
  } from "./stores/results-filter.js";
  import axios from "axios";
  import Header from "./common/Header.svelte";
  import Question from "./question/Question.svelte";
  import Search from "./search/Search.svelte";

  let searchData;
  let questionId;
  let questionTitle;
  let totalResults;
  let isLoading = true;
  let extensionAction;
  let selectedTag;
  let tagData;
  let initialInstruction = true;
  let errorObj;

  window.addEventListener("message", event => {
    extensionAction = event.data.action;

    if (event.data.action === "search") {
      searchQuery.set(event.data.query);
      selectedSearchFilter.set("Relevance");
      search();
      section.set("search");
    }

    if (event.data.action === "searchError") {
      searchQuery.set(event.data.query.error);
      selectedSearchFilter.set("Relevance");
      search();
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

  function handlePageSearch() {

  }

  function handleFilterChangeSearch() {

  }

  function handleTagFromQuestionSearch(event) {
    handleTagSelected(event);
  }

  // Search by selected tag - Only gets the wiki info -
  // Full search still needs to be done based on tag name with added property &tagged= to uri
  function handleTagSelected(event) {
    vscodeProgress("start", "Loading Tag Results", false);
    isLoading = true;
    window.scroll({ top: 0, behavior: "smooth" });
    selectedTag = event.detail.tag;

    const uri = `https://api.stackexchange.com/2.2/tags/${selectedTag}/wikis?site=stackoverflow&filter=!9_bDDrGXY`;

    axios
      .get(uri)
      .then(response => {
        if (response.status === 200) {
          tagData = response.data.items[0]
          // section.set("tag");
        }
        if(tagData === undefined) {
          tagData = { tag_name: selectedTag, error_msg: "No wiki found for given tag :("}
        }
      })
      .catch(() => {

      })
      .finally(() => {
        isLoading = false;
        vscodeProgress("stop", null, true);
        addCopyOption();
      })
  }

  // Main search functionality
  function search() {

    if($searchQuery.length !== 0){
      initialInstruction = false;
    }

    if (
      $searchQuery[0] === "[" &&
      $searchQuery[$searchQuery.length - 1] === "]"
    ) {
      console.log("tag search...")
      const tag = $searchQuery.substring(1, $searchQuery.length - 1);
      handleTagSelected({ detail: { tag: tag } });
      errorObj = null;
      return;
    }

    console.log("query search...")
    vscodeProgress("start", "Loading Search Results", false);
    isLoading = true;
    tagData = null;
    selectedTag = null;
    errorObj = null;

    const uri = `https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=relevance&q=${$searchQuery}&site=stackoverflow&filter=withbody`;

    axios
      .get(uri)
      .then(response => {
        isLoading = false;
        console.log(response.data)
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
</script>

<Header on:goBack={handleGotoSearch} {extensionAction} />

{#if $section === "search"}
  <Search
    on:gotoQuestion={handleGotoQuestion}
    on:gotoTagLearnMore={() => section.set("tag")}
    on:searchByTag={handleTagSelected}
    on:searchInput={search}
    on:searchByPage={handlePageSearch}
    on:filterChange={handleFilterChangeSearch}
    {isLoading}
    {searchData}
    {tagData}
    {totalResults}
    {initialInstruction}
    {errorObj}
  />
{:else if $section === "question"}
  <Question
    on:searchByTag={handleTagFromQuestionSearch}
    {questionId}
    {questionTitle}
    {extensionAction}
  />
{/if}