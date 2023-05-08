<script setup>
</script>

<template>
  <!-- @submit handles any form of submission. -->
  <!-- .prevent keeps the event from bubbling around and doing anything else. -->
  <!-- modal z-index has to be greater than 10  because the Code.vue component has z-10 -->

  <!-- backdrop -->
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-20">
    <div
      class="fixed top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] bg-white rounded-lg w-10/12 sm:6/12 lg:w-4/12  p-5 z-30">
      <header class="relative">
        <h5 class="text-xl font-medium text-left mb-3">
          Join us on Slack
        </h5>
        <button class="absolute top-0 right-0  translate-y-[-50%] p-0 text-gray-400 hover:text-gray-800" type="button"
                @click="close">
          x
        </button>
      </header>
      <section class="modal-body">
        <form @submit.prevent="handleSubmit">
          <div class="mb-4">
            <label for="email" class="block mb-2 text-sm font-medium text-gray-900 text-left">Your email</label>
            <input type="email" name="email" v-model="email"
                   class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 w-full p-2.5"
                   placeholder="name@gmail.com" required>
          </div>
          <button type="submit"
                  id="slackSubmit"
                  :disabled="submitState.disabled"
                  class="w-full text-white  focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
                  v-bind:class="{
                    'bg-blue-700 hover:bg-blue-800': submitState.state === 'fresh',
                    'bg-gray-300 hover:bg-gray-300': submitState.state === 'submitted',
                    'bg-green-700 hover:bg-green-800': submitState.state === 'success',
                    'bg-red-700 hover:bg-red-800': submitState.state === 'error'
                  }"

          >
            {{ submitState.text }}
          </button>
        </form>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      submitState: {
        state: 'fresh',
        disabled: false,
        text: "Join Slack",

      }
    }
  },
  methods: {
    async handleSubmit() {
      // this.$emit('submit', this.email)
      this.submitState.text = "Submitted";
      this.submitState.state = "submitted";
      this.submitState.disabled = true;
      const baseOptions = {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'x-api-key': `${import.meta.env.VITE_SLACK_API_KEY}`}
      };
      try {
        const body = JSON.stringify({email:this.email});
        console.log("body", body);
        const options = {...baseOptions, body: body};
        console.log("options", options);
        await fetch(`${import.meta.env.VITE_SLACK_API_ENDPOINT}`, options).then(response => response.json()).then(
          response => {
            // console.log(response);
            if (response.ok === true) {
              this.submitState.state = "success";
              this.submitState.text = "Success, Check your email";
            } else {
              this.submitState.state = "error";
              this.submitState.disabled = false;
              this.submitState.text = response.error.replace(/_/g, ' ');
            }
          }
        );
      } catch (error) {
        console.log(error);
        this.submitState.text = "Failed.";
        this.submitState.state = "error";
        this.submitState.disabled = false;
      }
    },
    close() {
      this.$emit('closeSlackModalEvent');
    },
  }
}

</script>

<style scoped></style>
