<template>
  <section id="talks" class="md:max-w-4xl mx-auto">
    <div class="bg-white border-b px-4 py-5 sm:px-6 shadow rounded-t-md">
      <div class="-ml-4 -mt-2 flex items-center justify-between flex-wrap sm:flex-nowrap">
        <div class="ml-4 mt-2">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Upcoming Events
          </h3>
        </div>
      </div>
    </div>
    <div class="bg-white shadow rounded-b-md">
      <ul class="divide-y divide-gray-200">
        <li v-for="talk in talks" :key="talk.link">
          <div class="p-4 sm:p-6">
            <a :href="talk.link" class="block hover:bg-gray-50">
              <p class="font-medium text-blue-600 truncate">{{ talk.name }}</p>
            </a>
            <p class="mt-2 flex items-center text-sm text-gray-500">
              <ClockIcon class="mr-1.5 h-5 w-5 text-gray-400" aria-hidden="true"/>
              <span class="truncate">{{ talk.time }}</span>
            </p>
            <p class="mt-2 flex items-center text-sm text-gray-500" v-if="talk.venue">
              <LocationMarkerIcon class="mr-1.5 h-5 w-5 text-gray-400" aria-hidden="true"/>
              <span class="truncate">{{ talk.venue }}</span>
            </p>
            <p class="mt-2 flex items-center text-sm text-gray-500">
              <UserCircleIcon class="mr-1.5 h-5 w-5 text-gray-400" aria-hidden="true"/>
              <span class="truncate">{{ talk.attendance }}</span>
            </p>
            <p class="mt-2 text-sm">
              <div class="talk-description" v-html="talk.description"></div>
            </p>
          </div>
        </li>
      </ul>
    </div>
  </section>
</template>

<script>
import {DateTime} from "luxon";

import {
  Dialog,
  DialogOverlay,
  DialogTitle,
  TransitionChild,
  TransitionRoot
} from '@headlessui/vue';

import {
  ChatAlt2Icon,
  ClockIcon,
  LocationMarkerIcon,
  UserCircleIcon,
  XIcon
} from '@heroicons/vue/outline';

export default {
  components: {
    Dialog,
    DialogOverlay,
    DialogTitle,
    TransitionChild,
    TransitionRoot,
    ChatAlt2Icon,
    ClockIcon,
    LocationMarkerIcon,
    UserCircleIcon,
    XIcon
  },
  data() {
    return {
      talks: [],
      form: {
        name: '',
        email: '',
        topic: ''
      },
      success: '',
      error: ''
    }
  },
  mounted() {
    this.fetchTalks()
  },
  methods: {
    async fetchTalks() {
      const cutOff = DateTime.now().plus({days: 90});
      const baseOptions = {
        method: 'GET',
        headers: {'Content-Type': 'application/json', 'x-api-key': `${import.meta.env.VITE_SLACK_API_KEY}`}
      };
      const response = await fetch(`${import.meta.env.VITE_API_URL}/events_list/`, baseOptions);
      const talks = await response.json();
      this.talks = talks.filter(talk => DateTime.fromMillis(talk.time) < cutOff).map(talk => {
        const time = DateTime.fromMillis(talk.time).toLocaleString(DateTime.DATETIME_FULL);
        const venue = talk.venue ? `${talk.venue.name} @ ${talk.venue.address_1} ${talk.venue.city}` : ''
        return {
          name: talk.name,
          time: time,
          venue: venue,
          attendance: talk.attendance,
          description: talk.description,
          link: talk.link
        }
      });
    }
  }
};
</script>

<style>
.talk-description a {
  color: rgb(37, 99, 235);
}

.talk-description p {
  margin-block-start: 1em;
  margin-block-end: 1em;
}
</style>
