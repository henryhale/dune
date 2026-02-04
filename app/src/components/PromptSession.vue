<script setup lang="ts">
import { useTodoStore } from '@/stores/todo';
import { useTemplateRef, watch } from 'vue';

const store = useTodoStore()

const logBoxRef = useTemplateRef < HTMLElement > ('logBoxRef');

watch([store.sessionLogs], () => {
    logBoxRef.value?.scrollTo({ behavior: 'smooth', top: logBoxRef.value?.scrollHeight })
})
</script>

<template>
    <div ref="logBoxRef" class="min-h-full">
        <div v-for="(c, i) in store.sessionLogs" :key="i" class="py-2 space-y-2">
            <div class="flex gap-1 bg-background p-1 rounded-lg">
                <div>
                    <div class="rounded-full px-2.5 py-1 bg-muted flex items-center justify-center">U</div>
                </div>
                <div class="p-1">{{ c.raw_text }}</div>
            </div>
            <div class="flex gap-1 p-1">
                <div>
                    <img src="/logo.png" alt="" class="rounded-full w-8" />
                </div>
                <div class="p-1">{{ c.command }} with <b>{{ (parseFloat(`${c.confidence}`) * 100).toFixed(4) }}%</b> confidence
                </div>
            </div>
        </div>
    </div>
</template>