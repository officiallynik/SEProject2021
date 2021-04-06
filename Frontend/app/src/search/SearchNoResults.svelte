<script>
  import { onMount } from "svelte";
  import { i18n } from "../stores/i18n.js";
  import { searchQuery } from "../stores/common.js";

  let query;

  onMount(() => {
    query = $searchQuery;
  });
</script>

<p>
  Sorry no results found :(
  <strong>
    <i>"{query}"</i>
    .
  </strong>
  Tip: Be less specific, try tagged search 
</p>
