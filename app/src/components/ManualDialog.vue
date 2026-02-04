<script setup lang="ts">
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import {
  Item,
  ItemContent,
  ItemDescription,
  ItemGroup,
  ItemSeparator,
  ItemTitle,
} from '@/components/ui/item'
import {COMMANDS as commands } from "@/stores/commands"
import {useTodoStore} from '@/stores/todo'
import { InfoIcon } from 'lucide-vue-next'
const store = useTodoStore()

</script>

<template>
  <Dialog :open="store.helpDialog" @update:open="store.helpDialog  = !store.helpDialog">
    <DialogTrigger as-child>
      <Button variant="ghost" size="icon">
        <InfoIcon />
      </Button>
    </DialogTrigger>
    <DialogContent class="sm:max-w-[425px]">
      <DialogHeader>
        <DialogTitle>Help</DialogTitle>
        <DialogDescription>
          A list of all available actions.
        </DialogDescription>
      </DialogHeader>
      <ItemGroup class="max-h-[50dvh] overflow-y-auto pb-8">
          <template v-for="(cmd, index) in Object.keys(commands)" :key="index">
              <Item>
              <ItemContent class="gap-1">
                  <ItemTitle>{{ cmd }}</ItemTitle>
                  <ItemDescription>{{ (commands as any)[cmd] }}</ItemDescription>
              </ItemContent>
              </Item>
              <ItemSeparator v-if="index !== Object.keys(commands).length - 1" />
          </template>
      </ItemGroup>
      <DialogFooter>
        <DialogClose as-child>
          <Button variant="outline">
            Close
          </Button>
        </DialogClose>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
