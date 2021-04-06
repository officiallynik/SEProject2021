<script>
  import SearchInput from "./SearchInput.svelte";
  import ResultsBar from "../Common/ResultsBar.svelte";
  import SearchItem from "./SearchItem.svelte";
  import SearchNoResults from "./SearchNoResults.svelte";
  import Loader from "../common/Loader.svelte";

  export let searchData;
  export let totalResults;
  export let tagData;
  export let isLoading;
</script>

<SearchInput {tagData} {isLoading} on:searchInput />

<ResultsBar {isLoading} />

{#if isLoading}
  <Loader />
{/if}

{#if searchData && totalResults !== 0}
  {console.log(searchData)}
  <SearchItem {isLoading} {searchData} on:gotoQuestion on:searchByTag />
{:else if !isLoading}
  <SearchNoResults />
{/if}

<!-- <SearchPager {totalResults} on:searchByPage /> -->