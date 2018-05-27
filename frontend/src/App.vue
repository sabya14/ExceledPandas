<template>
  <div class="row" style="margin: 0 auto; width: 100%;" id="app">
    <router-view :key="$route.fullPath"></router-view>
  </div>
</template>

<script>
  export default {
    name: 'App'
  }
</script>

