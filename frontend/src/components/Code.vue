<template>
    <section id="code" class="mt-16 max-w-md mx-auto relative z-10 px-4 sm:max-w-3xl sm:px-6 lg:max-w-7xl lg:px-8" aria-labelledby="contact-heading">
        <h2 class="sr-only" id="contact-heading">Contact us</h2>
        <div class="grid grid-cols-1 gap-y-20 lg:grid-cols-3 lg:gap-y-0 lg:gap-x-8">
            <div class="flex flex-col bg-white rounded-2xl shadow-xl">
                <div class="flex-1 relative pt-16 px-6 pb-8 md:px-8">
                <div class="absolute top-0 p-5 inline-block border-blue-600 rounded-xl shadow-lg transform -translate-y-1/2">
                    <Github class="h-6 w-6 text-white" aria-hidden="true" />
                </div>
                    <h3 class="text-xl font-medium text-blue-gray-900">Code With Us!</h3>
                    <p class="mt-4 text-base text-blue-gray-500">Fork us on Github</p>
                    <p class="mt-4 text-base text-blue-gray-500">
                        <a class="text-blue-500" href="https://github.com/bendog/pythonwa">
                            https://github.com/bendog/pythonwa
                        </a>
                    </p>
                </div>
            </div>
            <div class="flex flex-col bg-white rounded-2xl shadow-xl">
                <div class="flex-1 relative pt-16 px-6 pb-8 md:px-8">
                <div class="absolute top-0 p-5 inline-block border-blue-600 rounded-xl shadow-lg transform -translate-y-1/2">
                    <Github class="h-6 w-6 text-white" aria-hidden="true" />
                </div>
                    <h3 class="text-xl font-medium text-blue-gray-900">Learning Resources</h3>
                    <p class="mt-4 text-base text-blue-gray-500">Learn Python by sorting fuel prices</p>
                    <p class="mt-4 text-base text-blue-gray-500">
                        <a class="text-blue-500" href="https://github.com/robinchew/workshop_notes">
                            https://github.com/robinchew/workshop_notes
                        </a>
                    </p>
                </div>
            </div>
            <div class="flex flex-col bg-white rounded-2xl shadow-xl">
                <div class="flex-1 relative pt-16 px-6 pb-8 md:px-8">
                <div class="absolute top-0 p-5 inline-block border-blue-600 rounded-xl shadow-lg transform -translate-y-1/2">
                    <Github class="h-6 w-6 text-white" aria-hidden="true" />
                </div>
                    <h3 class="text-xl font-medium text-blue-gray-900">You?</h3>
                    <p class="mt-4 text-base text-blue-gray-500">Send us your code to be featured on the Python WA website</p>
                    <p class="mt-4 text-base text-blue-gray-500">
                        <a class="text-blue-500" href="https://github.com/">
                            https://github.com/
                        </a>
                    </p>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import Github from './Github.vue';

export default {
    components: {
        Github
    }
};
</script>
