
import type { Task, Command } from '@/types';

export const INITIAL_TASKS: Task[] = [
  { id: '1', content: 'Buy groceries', done: false },
  { id: '2', content: 'Schedule dentist appointment', done: false },
  { id: '3', content: 'Finish project report', done: true },
  { id: '4', content: 'Call mom', done: false, },
  { id: '5', content: 'Go for a run', done: false },
];

export const COMMANDS: Record<Command, string> = {
  "HELP": "Provides information on available commands.",
  "EXPLAIN": "Explains a specific command. (e.g., 'explain create')",
  "CONFIRM": "Confirms a pending action (like deletion).",
  "CANCEL": "Cancels an ongoing action or closes a form.",
  "REPEAT": "Repeats the last executed command.",
  "UNDO": "Reverts the last change to the task list.",
  "REDO": "Re-applies an undone change.",
  "ITEM_VIEW": "Displays details for a task. (e.g., 'view task Buy groceries')",
  "ITEM_PREV": "Selects the previous task in the list.",
  "ITEM_NEXT": "Selects the next task in the list.",
  "ITEM_SELECT": "Selects a task. (e.g., 'select task Call mom')",
  "GO_BACK": "Navigates back from a modal or view.",
  "GO_TO": "Navigates to a page. (e.g., 'go to completed', 'go to help')",
  "FILL_FIELD": "Fills a form field. (Not implemented via voice)",
  "CLEAR_FIELD": "Clears a form field. (Not implemented via voice)",
  "SUBMIT_FORM": "Submits the data in a form. (Triggered in modal)",
  "CANCEL_FORM": "Discards changes in a form.",
  "SEARCH": "Searches for tasks. (Not fully implemented, use filters)",
  "CREATE_ITEM": "Creates a new task. (e.g., 'create task Walk the dog due tomorrow')",
  "EDIT_ITEM": "Modifies a task. (e.g., 'edit task Buy groceries set status to completed')",
  "DELETE_ITEM": "Deletes a task. (e.g., 'delete task Go for a run')",
  "NOOP": "No operation; command not recognized."
};
