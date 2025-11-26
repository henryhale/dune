<script setup>
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { useTodoStore } from "@/stores/todo";
import { ArrowUpIcon, Loader2Icon, MicIcon } from 'lucide-vue-next';
import { ref } from "vue";
import VoiceArea from "./VoiceArea.vue";


const store = useTodoStore()

const handleSubmit = () => {
    if (store.isProcessing) return
    console.log('prompt:', store.commandInput)
    store.handleCommand()
}
</script>

<template>
    <Textarea @keyup.prevent.enter="handleSubmit" v-model.trim="store.commandInput"
        rows="3" placeholder="How can I help you?" class="pr-10"></Textarea>
    <div class="flex items-center">
        <span class="flex-grow italic px-1 opacity-60 text-xs">
            {{ store.isProcessing ? "processing..." : "" }}
        </span>
        <VoiceArea />
        <Button :disabled="store.isProcessing" @click.prevent="handleSubmit" size="icon" class="rounded-full">
            <Loader2Icon v-if="store.isProcessing" class="animate-spin" />
            <ArrowUpIcon v-else />
        </Button>
    </div>
</template>