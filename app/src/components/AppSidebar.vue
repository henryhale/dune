<script setup lang="ts">
import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarHeader,
    SidebarInset,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    SidebarProvider,
    SidebarRail,
    SidebarTrigger,
} from '@/components/ui/sidebar'
import { Button } from "@/components/ui/button"
import AppSettings from './AppSettings.vue';
import AppSearch from './AppSearch.vue';
import PromptArea from './PromptArea.vue';
import { HomeIcon, PenLineIcon, PlusIcon, SearchIcon, SparkleIcon, TrashIcon } from 'lucide-vue-next';
import { RouterLink } from 'vue-router';
import { ref } from 'vue';
import PromptSession from './PromptSession.vue';
import ManualDialog from './ManualDialog.vue';

const panel = ref(false)
</script>

<template>
    <SidebarProvider :default-open="true" storage-key="sidebar" class="flex min-h-screen">
        <Sidebar>
            <SidebarHeader>
                <SidebarMenu>
                    <SidebarMenuItem>
                        <SidebarMenuButton size="lg">
                            <div
                                class="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                                <PenLineIcon class="size-4" />
                            </div>
                            <div class="font-semibold text-lg flex-grow">Dunote</div>
                            <span
                                class="truncate text-sm rounded-xl px-2 border bg-accent text-accent-foreground">Free</span>
                        </SidebarMenuButton>
                    </SidebarMenuItem>
                </SidebarMenu>
            </SidebarHeader>
            <SidebarContent>
                <SidebarGroup>
                    <SidebarGroupLabel>Platform</SidebarGroupLabel>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            <SidebarMenuItem>
                                <SidebarMenuButton as-child>
                                    <RouterLink to="/">
                                        <HomeIcon />
                                        <span>Home</span>
                                    </RouterLink>
                                </SidebarMenuButton>
                            </SidebarMenuItem>
                            <SidebarMenuItem>
                                <SidebarMenuButton as-child>
                                    <RouterLink to="/search">
                                        <SearchIcon />
                                        <span>Search</span>
                                    </RouterLink>
                                </SidebarMenuButton>
                            </SidebarMenuItem>
                            <SidebarMenuItem>
                                <SidebarMenuButton as-child>
                                    <RouterLink to="/new">
                                        <PlusIcon />
                                        <span>New note</span>
                                    </RouterLink>
                                </SidebarMenuButton>
                            </SidebarMenuItem>
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>
            </SidebarContent>
            <SidebarFooter>
                <AppSettings />
            </SidebarFooter>
            <SidebarRail />
        </Sidebar>
        <SidebarInset class="max-h-screen overflow-hidden">
            <header
                class="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-12">
                <div class="flex items-center gap-2 px-4 w-full">
                    <SidebarTrigger class="-ml-1" />
                    <div class="flex-grow"></div>
                    <AppSearch />
                    <Button @click="panel = !panel" variant="default">
                        <SparkleIcon />
                        {{ panel ? "" : "Dune AI" }}
                    </Button>
                </div>
            </header>
            <div class="flex flex-1 flex-col gap-4 p-4 pt-0 overflow-y-auto">
                <slot></slot>
            </div>
        </SidebarInset>

        <Sidebar v-show="panel" side="right" collapsible="none"
            class="min-h-screen transition-all duration-200 font-mono border-l">
            <SidebarHeader>
                <div class="flex items-center gap-4 pl-2.5 py-2 pr-1">
                    <span class="flex-grow">Dune AI</span>
                    <!-- <Button @click="panel = false" size="icon" variant="ghost">
                        <XIcon />
                    </Button> -->
                    <ManualDialog />
                </div>
            </SidebarHeader>
            <SidebarContent>
                <SidebarGroup>
                    <SidebarGroupLabel class="flex items-center gap-4">
                        <span class="flex-grow">Session</span>
                        <Button size="icon" variant="ghost" class="hover:text-red-500 dark:hover:text-red-300">
                            <TrashIcon />
                        </Button>
                    </SidebarGroupLabel>
                    <SidebarGroupContent class="overflow-y-auto max-h-[65dvh] shadow-inner">
                        <PromptSession />
                    </SidebarGroupContent>
                </SidebarGroup>
            </SidebarContent>
            <SidebarFooter>
                <PromptArea />
            </SidebarFooter>
        </Sidebar>
    </SidebarProvider>
</template>
