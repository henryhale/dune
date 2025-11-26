<script setup>
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogFooter, AlertDialogDescription, AlertDialogTitle, AlertDialogHeader, AlertDialogTrigger } from '@/components/ui/alert-dialog';
import { TrashIcon } from 'lucide-vue-next';

const props = defineProps(["open"])
const emit = defineEmits(['update:open', 'confirm'])
</script>

<template>
    <AlertDialog :open="open" @update:open="emit('update:open')">
        <AlertDialogContent>
            <AlertDialogTrigger as-child>
                <slot></slot>
            </AlertDialogTrigger>
            <AlertDialogHeader>
                <AlertDialogTitle class="text-destructive">Confirm Deletion</AlertDialogTitle>
                <AlertDialogDescription>
                    Are you absolutely sure you want to delete this task? This action cannot be undone.
                </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
                <AlertDialogCancel>Cancel</AlertDialogCancel>
                <AlertDialogAction @click="emit('confirm')" class="bg-destructive text-destructive-foreground hover:bg-destructive/90">
                    <TrashIcon class="w-4 h-4 mr-1" /> Confirm Delete
                </AlertDialogAction>
            </AlertDialogFooter>
        </AlertDialogContent>
    </AlertDialog>
</template>