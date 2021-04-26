<!--
  display message on no result
-->
<script>
  import { onMount } from "svelte";
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
  Tip: Be less specific, try different combination of words
</p>
