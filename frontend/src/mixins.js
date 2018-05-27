import Vue from 'vue'
import $ from 'jquery'

export default Vue.mixin({
  methods: {
    ajaxCallPromise: function (param) {
      let self = this
      return new Promise(function (resolve, reject) {
        $.ajax({
          url: param.url,
          type: param.method,
          data: param.data,
          success: function (data, status, xhr) {
            self.setUser(xhr)
            self.loadingScreen = false
            if (data) {
              resolve(data)
            } else {
              resolve(true)
            }
          },
          error: function (errorData) {
            self.loadingScreen = false
            reject(errorData)
          }
        })
      })
    },
    getBaseUrl: function () {
      let baseUrl = window.location.protocol + '//' + window.location.hostname + ':8000'
      return baseUrl
    }
  }
})
