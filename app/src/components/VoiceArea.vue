<script setup lang="ts">
import { watch } from 'vue'
import { useSpeechRecognition } from '@vueuse/core';
import { Button } from './ui/button';
import { useTodoStore } from '@/stores/todo';
import { MicIcon, SquareStopIcon } from 'lucide-vue-next';


const store = useTodoStore()

const emit = defineEmits(['result'])

const { isListening, isSupported, start, stop, result, isFinal } = useSpeechRecognition({
    continuous: true,
    interimResults: true,
    lang: 'en-US',
})

let tid: number | undefined = undefined
watch([isFinal, result], ([final, transcript]) => {
    if (final && transcript) {
        store.commandInput = transcript
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
    <Button v-if="isSupported" @click="toggle" :disabled="store.isProcessing" size="icon" variant="ghost"
        class="rounded-full">
        <MicIcon v-if="!isListening" />
        <SquareStopIcon v-else />
    </Button>
</template>
