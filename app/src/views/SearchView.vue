<script setup>
import TaskList from '@/components/TaskList.vue';
import { useTodoStore } from '@/stores/todo';
import { useUrlSearchParams } from '@vueuse/core';
import { computed, watchEffect } from 'vue';


const store = useTodoStore()
const params = useUrlSearchParams()
</script>

<template>
    <div class="grid auto-rows-min gap-1 md:grid-cols-1 max-w-2xl mx-auto container">
        <div class="my-10">
            <h2 class="text-xl md:text-2xl font-semibold">Search</h2>
            <p class="opacity-60">Showing results for <q>{{ store.searchTerm || params.k }}</q></p>
        </div>
        <TaskList :items="store.filteredTodos" />
    </div>
</template>