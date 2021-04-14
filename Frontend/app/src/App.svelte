<script>
  import { page, section, searchQuery } from "./stores/common.js";
  import { vscodeProgress } from "./stores/vscode-api.js";
  import {
    selectedSearchFilter
  } from "./stores/results-filter.js";
  import axios from "axios";
  import Header from "./common/Header.svelte";
  import Question from "./question/Question.svelte";
  import Search from "./search/Search.svelte";
  import Tag from "./tag/tag.svelte";

  let searchData;
  let questionId;
  let questionTitle;
  let totalResults;
  let isLoading = true;
  let extensionAction;
  let selectedTag;
  let tagData;
  let gif;
  let showInstructions = true;

  window.addEventListener("message", event => {
    console.log(event);
    extensionAction = event.data.action;

    if (event.data.action === "search") {
      searchQuery.set(event.data.query);
      
      if(event.data.query){
        showInstructions = false;
        selectedSearchFilter.set("Relevance");
        search();
      }
      
      section.set("search");
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
    if (!selectedTag) {
      window.scroll({ top: 80, behavior: "smooth" });
      search();
    } else {
      window.scroll({ top: 0, behavior: "smooth" });
      tagSearch(selectedTag);
    }
  }

  function handleFilterChangeSearch() {
    page.set(1);
    !selectedTag ? search() : tagSearch(selectedTag);
  }

  function handleTagFromQuestionSearch(event) {
    section.set("search");
    handleTagSelected(event);
  }

  // Search by selected tag - Only gets the wiki info -
  // Full search still needs to be done based on tag name with added property &tagged= to uri
  function handleTagSelected(event) {
    vscodeProgress("start", "Loading Tag Results", false);
    isLoading = true;
    window.scroll({ top: 0, behavior: "smooth" });
    selectedTag = event.detail.tag;
    page.set(1);

    const uri = `https://stackoverflow.com/tags/${selectedTag}/wikis?site=&filter=&key=`;

    axios
      .get(uri)
      .then(response => {
        if (response.status === 200) {
          tagData = response.data.items[0];
          tagSearch(selectedTag);
        } else {
          isLoading = false;
          vscodeProgress("stop", null, true);
        }
      })
      .catch(() => {
        isLoading = false;
        vscodeProgress("stop", null, true);
      });
  }

  function tagSearch(selectedTag) {
    isLoading = true;
    searchQuery.set(`[${selectedTag}]`);

    const uri = `https://stackoverflow.com/search/advanced?tagged=${selectedTag}&page=${$page}&pagesize=10&order=${$selectedSearchFilter.apiOrder}&sort=${$selectedSearchFilter.apiSort}&site=&filter=&key=`;

    axios
      .get(uri)
      .then(response => {
        isLoading = false;
        if (response.status === 200) {
          searchData = response.data.items;
          totalResults = response.data.total;
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

  // Main search functionality
  function search() {
    console.log("searching...")

    vscodeProgress("start", "Loading Search Results", false);
    isLoading = true;
    tagData = null;
    selectedTag = null;

    const uri = `https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=Relevance&q=${$searchQuery}&site=stackoverflow&filter=withbody`;

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

  // function scrollTop() {
  //   document.documentElement.animate({scrollTop: 0});
  // }
</script>

<!-- <style>
#topBtn {
  display: inline-block;
  background: url('topBtn.png');
  width: 50px;
  height: 50px;
  text-align: center;
  border-radius: 4px;
  position: fixed;
  bottom: 30px;
  right: 30px;
  transition: background-color .3s, 
    opacity .5s, visibility .5s;
  opacity: 1;
  visibility: visible;
  z-index: 1000;
}
#topBtn:hover {
  cursor: pointer;
  background-color: #333;
}
#topBtn:active {
  background-color: #555;
}
</style> -->

<!-- svelte-ignore a11y-missing-attribute
<!-- svelte-ignore a11y-missing-content -->
<!-- <a id="topBtn" on:click={scrollTop}></a> -->

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
    {showInstructions}
  />
{:else if $section === "question"}
  <Question
    on:searchByTag={handleTagFromQuestionSearch}
    {questionId}
    {questionTitle}
    {extensionAction}
    {gif}
  />
{:else if $section === "tag"}
  <Tag {tagData} />
{/if}