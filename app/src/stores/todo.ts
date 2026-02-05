import { PREDICTION_API } from "@/api";
import type { APIResult, Task } from "@/types";
import { defineStore } from "pinia"
import { ref, computed, watch } from "vue"
import { useRouter } from "vue-router";
import { toast } from 'vue-sonner'



export const useTodoStore = defineStore('todo', () => {
    const router = useRouter()

    // State
    const todos = ref<Task[]>([
        { id: 1, content: 'Buy groceries', done: false },
        { id: 2, content: 'Finish project report', done: false },
        { id: 3, content: 'Call dentist', done: true }
    ]);
    const newTodo = ref('')
    const commandInput = ref('');
    const selectedIndex = ref(0);
    const isProcessing = ref(false);
    const feedback = ref({ message: '', type: 'info' });
    const history = ref<any[]>([]);
    const historyIndex = ref(-1);
    const searchQuery = ref('');
    const editingId = ref<string>();
    const editText = ref('');
    const todoListRef = ref<HTMLElement>();
    const alertDialog = ref(false)
    const deletingId = ref<string>()
    const sessionLogs = ref<APIResult[]>([])
    const helpDialog = ref(false)

    // Computed (Getters)
    const filteredTodos = computed(() => {
        if (!searchQuery.value) return todos.value;
        return todos.value.filter(t =>
            t.content.toLowerCase().includes(searchQuery.value.toLowerCase())
        );
    });

    const totalTodos = computed(() => todos.value.length);

    const completedTodos = computed(() =>
        todos.value.filter(t => t.done).length
    );

    // Watchers
    watch(() => feedback.value.message, (value) => {
        if (value) {
            setTimeout(() => {
                feedback.value.message = '';
            }, 3000);
        }
    });

    // Actions
    function showFeedback(message: string, type: 'info' | 'success' | 'error' | 'warning' = 'info') {
        feedback.value = { message, type };
        switch (type) {
            case 'info':
                toast.info(message)
                break;
            case 'success':
                toast.success(message)
                break;
            case 'error':
                toast.error(message)
                break;
            case 'warning':
                toast.warning(message)
                break;

            default:
                toast(message)
                break;
        }
    }

    function saveToHistory() {
        history.value = [
            ...history.value.slice(0, historyIndex.value + 1) as any,
            JSON.parse(JSON.stringify(todos.value))
        ];
        historyIndex.value++;
    }

    function viewTodo() {
        const todo = todos.value[selectedIndex.value]
        if (!todo) return
        const pages = {
            search: '/search',
            home: '/',
            new: "/new",
            note: '/new',
            view: `/view/${todo.id}`,
            edit: `/view/${todo.id}/edit`,
        }
        const scores: Record<string, string> = {}
        const parts = commandInput.value.toLowerCase().split(' ')
        let bestguess, previous = 0
        for (const key of Object.keys(pages)) {
            let score = parts.map(p => key.includes(p) || p.includes(key)).reduce((s, x) => s + (x ? 1 : 0), 0)
            if (score > previous) {
                bestguess = scores[key]
            }
        }
        if (bestguess) {
            router.push(bestguess)
        }
    }

    async function handleCommand() {
        const input = commandInput.value.trim();

        if (!input) return;

        isProcessing.value = true;

        try {
            const result = await PREDICTION_API.makePrediction(input);

            if (result.status === 'success' && result.action) {
                executeCommand(result.action.command, input);
                showFeedback(`Command executed: ${result.action.command}`, 'success');
            } else {
                showFeedback(result.message || 'Command not recognized', 'error');
            }
            sessionLogs.value.push(result.action as APIResult)
            commandInput.value = '';
        } catch (error) {
            showFeedback('Error processing request', 'error');
            console.error('API Error:', error);
        } finally {
            isProcessing.value = false;
        }
    }

    function executeCommand(command: string, originalText: string) {
        const text = originalText.toLowerCase();

        switch (command) {
            case 'HELP':
                showFeedback('Available commands: add task, mark complete, delete task, next/previous, search, etc.', 'info');
                helpDialog.value = true
                break;

            case 'EXPLAIN':
                const selected = todos.value[selectedIndex.value];
                if (selected) {
                    showFeedback(`Task: "${selected.content}" - ${selected.done ? 'Completed' : 'Not completed'}`, 'info');
                }
                break;

            case 'CONFIRM':
                if (selectedIndex.value >= 0 && selectedIndex.value < todos.value.length) {
                    saveToHistory();
                    todos.value[selectedIndex.value]!.done = true;
                    showFeedback('Task marked as complete', 'success');
                } else if (deletingId.value && alertDialog.value) {
                    deleteTodo(deletingId.value)
                    alertDialog.value = false
                    deletingId.value = undefined
                } else {
                    helpDialog.value = false
                }
                break;

            case 'CANCEL':
                editingId.value = undefined;
                searchQuery.value = '';
                alertDialog.value = false
                helpDialog.value = false
                showFeedback('Action cancelled', 'info');
                break;

            case 'UNDO':
                if (historyIndex.value >= 0) {
                    todos.value = JSON.parse(JSON.stringify(history.value[historyIndex.value]));
                    historyIndex.value--;
                    showFeedback('Undo successful', 'success');
                }
                break;

            case 'REDO':
                if (historyIndex.value < history.value.length - 1) {
                    historyIndex.value++;
                    todos.value = JSON.parse(JSON.stringify(history.value[historyIndex.value]));
                    showFeedback('Redo successful', 'success');
                }
                break;

            case 'REPEAT':
                if (history.value.length > 0) {
                    showFeedback('Repeating last action...', 'info');
                }
                break;

            case 'GO_BACK':
                if (editingId.value) {
                    editingId.value = undefined;
                    showFeedback('Exited edit mode', 'info');
                } else if (deletingId.value) {
                    deletingId.value = undefined
                    alertDialog.value = false
                } else {
                    router.back()
                }
                searchQuery.value = ''
                break;

            case 'GO_TO':
                const match = text.match(/\d+/);
                if (match) {
                    const index = parseInt(match[0]) - 1;
                    if (index >= 0 && index < todos.value.length) {
                        selectedIndex.value = index;
                        showFeedback(`Navigated to task ${index + 1}`, 'success');
                    }
                } else {
                    viewTodo()

                    helpDialog.value = false
                }
                break;

            case 'SCROLL_UP':
                todoListRef.value?.scrollBy({ top: -100, behavior: 'smooth' });
                break;

            case 'SCROLL_DOWN':
                todoListRef.value?.scrollBy({ top: 100, behavior: 'smooth' });
                break;

            case 'NEXT_ITEM':
                selectedIndex.value = Math.min(selectedIndex.value + 1, todos.value.length - 1);
                showFeedback(`Selected task ${Math.min(selectedIndex.value + 1, todos.value.length)}`, 'info');
                break;

            case 'PREVIOUS_ITEM':
                selectedIndex.value = Math.max(selectedIndex.value - 1, 0);
                showFeedback(`Selected task ${Math.max(selectedIndex.value + 1, 1)}`, 'info');
                break;

            case 'SELECT_ITEM':
                if (selectedIndex.value >= 0 && selectedIndex.value < todos.value.length) {
                    saveToHistory();
                    todos.value[selectedIndex.value]!.done = !todos.value[selectedIndex.value]!.done;
                    showFeedback('Task toggled', 'success');
                } else if (selectedIndex.value) {
                    router.push(`/view/${todos.value[selectedIndex.value]?.id ?? -1}`)
                    showFeedback('Viewing task details', 'info')
                }
                break;

            case 'VIEW_ITEM':
                if (selectedIndex.value) {
                    router.push(`/view/${todos.value[selectedIndex.value]?.id ?? -1}`)
                    showFeedback('Viewing task details', 'info')
                }
                break;

            case 'SEARCH':
                const searchMatch = text.match(/search (?:for )?(.+)/);
                if (searchMatch) {
                    searchQuery.value = searchMatch[1] || "";
                    showFeedback(`Searching for: ${searchMatch[1]}`, 'info');
                    router.push(`/search/?k=${encodeURI(searchQuery.value)}`)
                }
                break;

            case 'FILL_FIELD':
                const fillMatch = text.match(/(?:add|create|new task) (.+)/);
                if (fillMatch) {
                    saveToHistory();
                    const newTodo: Task = {
                        id: Date.now().toString(),
                        content: fillMatch[1] || "",
                        done: false
                    };
                    todos.value.push(newTodo);
                    showFeedback('Task added', 'success');
                }
                break;

            case 'CLEAR_FIELD':
                searchQuery.value = '';
                editText.value = '';
                newTodo.value = ''
                showFeedback('Field cleared', 'info');
                break;

            case 'SUBMIT_FORM':
                if (editingId.value) {
                    saveToHistory();
                    const todo = todos.value.find(t => t.id === editingId.value);
                    if (todo) {
                        todo.content = editText.value;
                    }
                    editingId.value = undefined;
                    showFeedback('Task updated', 'success');
                } else if (newTodo.value) {
                    saveTodo()
                }
                break;

            case 'NOOP':
                break;

            default:
                showFeedback('Command not recognized', 'warning');
        }
    }

    function toggleTodo(id: string) {
        saveToHistory();
        const todo = todos.value.find(t => t.id === id);
        if (todo) {
            todo.done = !todo.done;
        }
    }

    function startDelete(id: string) {
        deletingId.value = id
        alertDialog.value = true
    }

    function deleteTodo(id: string) {
        saveToHistory();
        todos.value = todos.value.filter(t => t.id !== id);
        showFeedback('Task deleted', 'success');
        alertDialog.value = false
    }

    function startEdit(todo: Task) {
        editingId.value = todo.id as string;
        editText.value = todo.content;
    }

    function submitEdit(id: string) {
        saveToHistory();
        const todo = todos.value.find(t => t.id === id);
        if (todo) {
            todo.content = editText.value;
        }
        editingId.value = undefined;
        showFeedback('Task updated', 'success');
    }

    function setTodoListRef(el: HTMLElement) {
        todoListRef.value = el;
    }

    function getTodo(id: string) {
        return todos.value.find((t) => t.id == id)
    }

    function saveTodo() {
        if (newTodo.value) {
            saveToHistory();
            todos.value.push({ id: Date.now(), content: newTodo.value, done: false })
            showFeedback("Task saved.", 'success')
        } else {
            showFeedback('Fill in the details to save.', 'info')
        }
    }


    // Return everything for the store
    return {
        // State
        todos,
        newTodo,
        commandInput,
        selectedIndex,
        isProcessing,
        feedback,
        history,
        historyIndex,
        searchQuery,
        editingId,
        editText,
        todoListRef,
        alertDialog,
        sessionLogs,
        helpDialog,
        // Computed
        filteredTodos,
        totalTodos,
        completedTodos,
        // Actions
        showFeedback,
        saveToHistory,
        handleCommand,
        executeCommand,
        toggleTodo,
        startDelete,
        deleteTodo,
        startEdit,
        submitEdit,
        setTodoListRef,
        getTodo,
        saveTodo
    };
});
