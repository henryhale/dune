<script setup>
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { PencilIcon, TrashIcon } from 'lucide-vue-next';
import { useRouter } from 'vue-router';
import { computed, ref } from 'vue';
import DeleteDialog from './DeleteDialog.vue';
import { useTodoStore } from '@/stores/todo';

const store = useTodoStore()
const router = useRouter()
const props = defineProps(['items'])

</script>

<template>
    <div :ref="store.todoListRef" class="grid auto-rows-min gap-1 md:grid-cols-1 max-h-96 overflow-y-auto">
        <p v-if="props.items.length === 0" class="my-10 opacity-50">No tasks here. Try adding one!</p>
        <div v-for="(n, i) in props.items" :key="i" :class="{
            'border border-current/40 outline-none rounded-xl': store.selectedIndex == i
        }" class="group relative cursor-pointer" tabindex="0" @click.stop="router.push(`/view/${n.id}`)">
            <div class="flex gap-2 items-start p-4 group-hover:bg-accent/20 rounded-xl">
                <div @click.prevent.stop="store.toggleTodo(n.id)" class="py-2">
                    <Checkbox :checked="n.done" />
                </div>
                <p class="flex-grow pt-1 line-clamp-4 leading-normal">
                    <s v-if="n.done">{{ n.content }}</s>
                    <span v-else>{{ n.content }}</span>
                </p>
            </div>
            <div class="absolute right-0 bottom-0 p-2 group-hover:block hidden space-x-2">
                <Button size="icon-sm" variant="ghost" class="opacity-50 hover:opacity-100"
                    @click.stop="router.push(`/view/${n.id}/edit`)">
                    <PencilIcon />
                </Button>
                <Button @click="store.startDelete(n.id)" size="icon-sm" variant="ghost"
                    class="opacity-50 hover:opacity-100" click="">
                    <TrashIcon />
                </Button>

            </div>
        </div>
        <DeleteDialog :open="store.alertDialog" @update:open="v => {
            store.alertDialog = v
        }" @confirm="store.deleteTodo(itemID)"></DeleteDialog>
    </div>
</template>
