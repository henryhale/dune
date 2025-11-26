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
    DropdownMenuShortcut,
    DropdownMenuSub,
    DropdownMenuSubContent,
    DropdownMenuSubTrigger,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { ArrowUpRightIcon, SettingsIcon } from 'lucide-vue-next'
import { useColorMode } from '@vueuse/core'

const mode = useColorMode()
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
                <DropdownMenuItem>
                    Keyboard shortcuts
                    <DropdownMenuShortcut>⌘K</DropdownMenuShortcut>
                </DropdownMenuItem>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
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
            <DropdownMenuItem>
                GitHub
                <ArrowUpRightIcon class="opacity-60 ml-auto" />
            </DropdownMenuItem>
            <DropdownMenuItem>
                Support
                <ArrowUpRightIcon class="opacity-60 ml-auto" />
            </DropdownMenuItem>
        </DropdownMenuContent>
    </DropdownMenu>
</template>
