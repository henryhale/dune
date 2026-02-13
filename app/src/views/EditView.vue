<script setup lang="ts">
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { XIcon } from 'lucide-vue-next';
import { useRouter } from 'vue-router';
import { onBeforeMount } from 'vue';
import { useTodoStore } from '@/stores/todo';

const props = defineProps(['id'])
const router = useRouter()
const store = useTodoStore()

const save = () => {
    store.submitEdit(props.id)
    router.push(`/view/${props.id}/`)
}

onBeforeMount(() => {
    const item = store.getTodo(props.id)
    if (!item) {
        router.replace('/not-found')
    } else {
        store.startEdit(item)
    } 
})
</script>

<template>
    <div class="min-h-[100vh] flex-1 rounded-xl md:min-h-min">
        <form @submit.prevent="save" class="container mx-auto max-w-2xl grid gap-4">
            <div class="flex items-center">
                <div class="flex-grow my-10">
                    <h2 class="text-xl md:text-2xl font-semibold">Edit Note</h2>
                    <p class="opacity-60">Something's change?</p>
                </div>
                <Button @click="router.push(`/view/${props.id}/`)" title="Cancel" type="button" variant="ghost"
                    class="rounded-full opacity-60" size="icon">
                    <XIcon />
                </Button>
            </div>
            <Textarea v-model.trim="store.editText" class="min-h-[40dvh] bg-muted/30"
                placeholder="Remember to ..."></Textarea>
            <div>
                <Button :disabled="!store.editText" type="submit" class="w-1/2">
                    Save
                </Button>
            </div>
        </form>
    </div>
</template>