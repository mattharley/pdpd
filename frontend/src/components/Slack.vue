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
            <input type="email" name="email"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 w-full p-2.5"
              placeholder="name@gmail.com" required>
          </div>
          <button type="submit"
            class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center">Submit</button>
        </form>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: ''
    }
  },
  methods: {
    async handleSubmit() {
      // this.$emit('submit', this.email)
      const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-api-key': `${import.meta.env.VITE_SLACK_API_KEY}` },
        body: `{"email":"${this.email}"}`
      };
      try {
        await fetch(`${import.meta.env.VITE_SLACK_API_ENDPOINT}`, options);
        alert("Email sent successfully")
        this.$emit('closeSlackModalEvent');
      } catch (error) {
        console.log(error)
        alert("unexpected error, please let us know")
      }
    },
    close() {
      this.$emit('closeSlackModalEvent');
    },
  }
}

</script>

<style scoped></style>