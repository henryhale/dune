<script setup lang="ts">
import { Button } from '@/components/ui/button'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuGroup,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuPortal,
    DropdownMenuSeparator,
    DropdownMenuSub,
    DropdownMenuSubContent,
    DropdownMenuSubTrigger,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { ArrowUpRightIcon, SettingsIcon } from 'lucide-vue-next'
import { useColorMode } from '@vueuse/core'

const mode = useColorMode()

const openExternalLink = (link: string) => {
    window.open(link, "_blank")
}
</script>

<template>
    <DropdownMenu>
        <DropdownMenuTrigger as-child>
            <Button variant="ghost" class="flex justify-start">
                <SettingsIcon />
                <span>Settings</span>
            </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent class="w-56" align="start">
            <DropdownMenuLabel>My Account</DropdownMenuLabel>
            <DropdownMenuGroup>
                <DropdownMenuSub>
                    <DropdownMenuSubTrigger>Theme</DropdownMenuSubTrigger>
                    <DropdownMenuPortal>
                        <DropdownMenuSubContent>
                            <DropdownMenuItem @click="mode = 'light'">Light</DropdownMenuItem>
                            <DropdownMenuItem @click="mode = 'dark'">Dark</DropdownMenuItem>
                            <DropdownMenuItem @click="mode = 'auto'">System</DropdownMenuItem>
                        </DropdownMenuSubContent>
                    </DropdownMenuPortal>
                </DropdownMenuSub>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="openExternalLink('https://github.com/henryhale/dune')">
                GitHub
                <ArrowUpRightIcon class="opacity-60 ml-auto" />
            </DropdownMenuItem>
            <DropdownMenuItem @click="openExternalLink('https://henryhale.github.io/contact')">
                Feedback
                <ArrowUpRightIcon class="opacity-60 ml-auto" />
            </DropdownMenuItem>
        </DropdownMenuContent>
    </DropdownMenu>
</template>
