<template>
  <div class="row" style="padding: 2% 0 0 0; width: 100%; text-align: center;">
    <label class="file-select">
      <div class="select-button">
        <span v-if="value">Selected File: {{value.name}}</span>
        <span v-else>Select File</span>
      </div>
      <input type="file" @change="handleFileChange"/>
    </label>
  </div>
</template>

<script>
  import FileUpload from 'vue-upload-component'

  export default {
    components: {
      FileUpload,
    },
    name: 'mainPage',
    data() {
      return {
        files: [],
        value: null
      }
    },
    methods: {
      handleFileChange(e) {
       this.value = e.target.files[0]
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .file-select > .select-button {
    padding: 1rem;

    color: white;
    background-color: #2EA169;

    border-radius: .3rem;

    text-align: center;
    font-weight: bold;
  }

  .file-select > input[type="file"] {
    display: none;
  }
</style>


style

>

