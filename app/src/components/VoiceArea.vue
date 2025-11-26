<script setup>
import { ref, watch } from 'vue'
import { useSpeechRecognition } from '@vueuse/core';
import { Button } from './ui/button';
import { useTodoStore } from '@/stores/todo';
import { MicIcon, SquareStopIcon } from 'lucide-vue-next';


const store = useTodoStore()

const emit = defineEmits(['result'])

const { isListening, isSupported, start, stop, transcript } = useSpeechRecognition({
    continuous: true,
    interimResults: true,
    lang: 'en-US',
})

let tid = undefined
watch(transcript, (val) => {
    if (val) {
        store.commandInput += val
        clearTimeout(tid)
        tid = setTimeout(() => {
            store.handleCommand()
        }, 100);
    }
})

const toggle = () => {
    isListening.value ? stop() : start()
}
</script>

<template>
    <Button @click="toggle" :disabled="isSupported || store.isProcessing" size="icon" variant="ghost" class="rounded-full">
        <MicIcon v-if="!isListening" />
        <SquareStopIcon v-else />
    </Button>
</template>
