<template>
  <div class="relative overflow-hidden">
    <div class="relative pt-6 pb-16 sm:pb-24">
      <Popover>
        <div class="max-w-7xl mx-auto px-4 sm:px-6">
          <nav class="relative flex items-center justify-between sm:h-10 md:justify-center" aria-label="Global">
            <div class="flex items-center flex-1 md:absolute md:inset-y-0 md:left-0">
              <div class="flex items-center justify-between w-full md:w-auto">
                <a href="#">
                  <span class="sr-only">Workflow</span>
                  <img class="h-8 w-auto sm:h-10" src="../assets/pythonwa.png" alt="" />
                </a>
                <div class="-mr-2 flex items-center md:hidden">
                  <PopoverButton
                    class="bg-gray-50 rounded-md p-2 inline-flex items-center justify-center text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500">
                    <span class="sr-only">Open main menu</span>
                    <MenuIcon class="h-6 w-6" aria-hidden="true" />
                  </PopoverButton>
                </div>
              </div>
            </div>
            <div class="hidden md:flex md:space-x-10">
              <a v-for="item in navigation" :key="item.name" :href="item.href"
                class="font-medium text-gray-500 hover:text-gray-900" v-smooth-scroll>{{ item.name }}</a>
            </div>
            <div class="hidden md:absolute md:flex md:items-center md:justify-end md:inset-y-0 md:right-0">
              <!-- <span class="inline-flex rounded-md shadow">
                <a href="#" class="inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md text-blue-400 bg-white hover:bg-gray-50">
                  Log in
                </a>
              </span> -->
            </div>
          </nav>
        </div>

        <transition enter-active-class="duration-150 ease-out" enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100" leave-active-class="duration-100 ease-in"
          leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
          <PopoverPanel focus class="absolute top-0 inset-x-0 p-2 transition transform origin-top-right md:hidden">
            <div class="rounded-lg shadow-md bg-white ring-1 ring-black ring-opacity-5 overflow-hidden">
              <div class="px-5 pt-4 flex items-center justify-between">
                <div>
                  <div class="h-8 w-auto">
                    <img class="h-8 w-auto sm:h-10" src="../assets/pythonwa.png" />
                  </div>
                </div>
                <div class="-mr-2">
                  <PopoverButton
                    class="bg-white rounded-md p-2 inline-flex items-center justify-center text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500">
                    <span class="sr-only">Close menu</span>
                    <XIcon class="h-6 w-6" aria-hidden="true" />
                  </PopoverButton>
                </div>
              </div>
              <div class="px-2 pt-2 pb-3">
                <a v-for="item in navigation" :key="item.name" :href="item.href"
                  class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50"
                  v-smooth-scroll>{{ item.name }}</a>
              </div>
              <!-- <a href="#" class="block w-full px-5 py-3 text-center font-medium text-blue-400 bg-gray-50 hover:bg-gray-100">
                Log in
              </a> -->
            </div>
          </PopoverPanel>
        </transition>
      </Popover>

      <main class="mt-16 mx-auto max-w-7xl px-4 sm:mt-24">
        <div class="text-center">
          <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
            <span class="block xl:inline">Welcome to the</span>
            {{ ' ' }}
            <span class="block text-blue-700 xl:inline">Python WA</span>
            {{ ' ' }}
            <span class="block xl:inline">website</span>
          </h1>
          <p class="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
            The Meetup Group for Perth-fectionists with Deadlines
          </p>
          <div class="mt-5 max-w-lg mx-auto sm:flex sm:justify-center md:mt-8">
            <div class="rounded-md shadow">
              <div
                class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:py-4 md:text-lg md:px-10"
                @click="showSlackModal">
                Chat with us <img class="ml-4 h-8" src="../assets/slack.png" />
              </div>
              <Slack v-show="isSlackModalVisible" @closeSlackModalEvent="closeSlackModal" />
            </div>
            <div class="mt-3 rounded-md shadow sm:mt-0 sm:ml-3">
              <a href="http://www.meetup.com/pythonwa/"
                class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-blue-600 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10">
                Join the group <img class="ml-4 h-8" src="../assets/meetup.png" />
              </a>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue';
import Slack from './Slack.vue'
import { MenuIcon, XIcon } from '@heroicons/vue/outline';

const navigation = [
  { name: 'Talks', href: '#talks' },
  { name: 'Photos', href: '#photos' },
  { name: 'Sponsors', href: '#sponsors' },
  { name: 'Code With Us', href: '#code' },
  { name: 'Conduct', href: '#conduct' },
];

export default {
  components: {
    Popover,
    PopoverButton,
    PopoverPanel,
    MenuIcon,
    XIcon,
    Slack
  },
  data() {
    return {
      isSlackModalVisible: false
    }
  },
  methods: {
    showSlackModal() {
      this.isSlackModalVisible = true;
    },
    closeSlackModal() {
      this.isSlackModalVisible = false;
    }
  },
  setup() {
    return {
      navigation,
    }
  },
};
</script>    
