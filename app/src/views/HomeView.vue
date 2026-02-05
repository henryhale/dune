<script setup lang="ts">
import TaskList from '@/components/TaskList.vue';
import { useTodoStore } from '@/stores/todo';

const store = useTodoStore()
</script>

<template>
    <div class="grid auto-rows-min gap-1 md:grid-cols-1 max-w-2xl mx-auto container">
        <h2 class="text-xl md:text-2xl font-semibold my-8">All Tasks</h2>
        <TaskList :items="store.filteredTodos" />
    </div>
</template>