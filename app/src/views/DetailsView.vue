<script setup lang="ts">
import { onBeforeMount, ref } from 'vue';
import { useRouter } from 'vue-router';
import { ArrowLeftIcon, PencilIcon, TrashIcon } from 'lucide-vue-next';
import { Button } from '@/components/ui/button';
import DeleteDialog from '@/components/DeleteDialog.vue';
import { useTodoStore } from '@/stores/todo';
import type { Task } from '@/types';

const props = defineProps(['id'])
const router = useRouter()
const store = useTodoStore()

const todo = ref<Task>()

onBeforeMount(() => {
    const item = store.getTodo(props.id?.toString() ?? "")
    if (!item) {
        router.replace('/not-found')
    } else {
        todo.value = item
    }
})

const initDelete = () => {
    store.startDelete(props.id)
}

const updateDeleteDialog = (v: boolean) => {
    store.alertDialog = v
}

const completeDelete = () => {
    store.deleteTodo(props.id)
}
</script>

<template>
    <div class="min-h-[90dvh] flex-1 rounded-xl bg-muted/50 md:min-h-min flex items-center justify-center relative">
        <div class="absolute bottom-0 right-0 left-0 p-2 opacity-50 flex space-x-2">
            <Button size="sm" variant="ghost" @click="router.push(`/`)">
                <ArrowLeftIcon />
                Back
            </Button>
            <div class="flex-grow"></div>
            <Button size="sm" variant="ghost" @click="router.push(`/view/${props.id}/edit`)">
                <PencilIcon />
                Edit
            </Button>
            <Button size="sm" variant="ghost" @click="initDelete">
                <TrashIcon />
                Delete
            </Button>
        </div>
        <p class="text-lg md:text-xl">
            {{ todo?.content ?? "" }}
        </p>
    </div>

    <DeleteDialog :open="store.alertDialog" @update:open="updateDeleteDialog" @confirm="completeDelete"></DeleteDialog>
</template>