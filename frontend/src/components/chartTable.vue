<template>
  <div id="chart_table">
    <div class="top_titles">
      <div class="small-12 medium-1 column"> id</div>
      <div class="small-12 medium-2 column"> Value</div>
      <div class="small-12 medium-6 column"> Label</div>
      <div class="small-12 medium-2 column"> icon</div>
      <div class="small-12 medium-1 column">
        <i class="fa fa-trash" aria-hidden="true"></i>
      </div>
    </div>
    <div :key=index v-for="(val, index) in proplabels" class="row table_cell">
      <div class="small-12 medium-1 column">
        <input type="text" v-model="val.id" disabled>
      </div>
      <div class="small-12 medium-2 column single-cel">
        <input type="text" v-model="val.percentual" v-bind:disabled="disabled">

      </div>
      <div class="small-12 medium-6 column single-cel">
        <input type="text" v-model="val.label" v-bind:disabled="disabled">
      </div>
      <div class="small-12 medium-2 column single-cel">
        <input type="text" v-model="val.icon" v-bind:disabled="disabled">
      </div>
      <div class="small-12 medium-1 column edit_panel">
        <button @click="deleteEvent(index)">
          <i class="fa fa-times" aria-hidden="true"></i>
        </button>
        <span class="edit_mode" @click="disabled = !disabled">
                <i class="fa fa-pencil-square-o" aria-hidden="true"></i>
            </span>
      </div>
    </div>


  </div>
</template>

<script>
  export default {
    props: ['proplabels'],
    data() {
      return {
        disabled: true
      }
    },
    methods: {
      deleteEvent: function (index) {
        this.proplabels.splice(index, 1);
      }
    }
  }
</script>

<style scoped>

</style>
