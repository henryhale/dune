<script setup>
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { useTodoStore } from '@/stores/todo';
import { XIcon } from 'lucide-vue-next';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

const router = useRouter()
const store = useTodoStore()

</script>

<template>
    <div class="min-h-[100vh] flex-1 rounded-xl md:min-h-min">
        <form @submit.prevent="store.newTodo && store.saveTodo()" class="container mx-auto max-w-2xl grid gap-4">
            <div class="flex items-center">
                <div class="flex-grow my-10">
                    <h2 class="text-xl md:text-2xl font-semibold">New Note</h2>
                    <p class="opacity-60">What do you have to do?</p>
                </div>
                <Button @click="router.push('/')" title="Cancel" type="button" variant="ghost"
                    class="rounded-full opacity-60" size="icon">
                    <XIcon />
                </Button>
            </div>
            <Textarea v-model.trim="store.newTodo" class="min-h-[40dvh] bg-muted/30" placeholder="I want to..."></Textarea>
            <div>
                <Button :disabled="!store.newTodo" type="submit" class="w-1/2">
                    Save
                </Button>
            </div>
        </form>
    </div>
</template>