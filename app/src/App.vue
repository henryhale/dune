<script setup lang="ts">
import 'vue-sonner/style.css'
import { Toaster } from '@/components/ui/sonner'
import AppSidebar from '@/components/AppSidebar.vue';
import { RouterView } from 'vue-router';

</script>

<template>
    <AppSidebar>
        <RouterView />
        <Toaster position="top-center" />
    </AppSidebar>
</template>