export interface Task {
  id: string | number;
  content: string;
  done: boolean;
}

export type Command =
  | 'HELP' | 'EXPLAIN' | 'CONFIRM' | 'CANCEL' | 'REPEAT' | 'UNDO' | 'REDO'
  | 'ITEM_VIEW' | 'ITEM_PREV' | 'ITEM_NEXT' | 'ITEM_SELECT'
  | 'GO_BACK' | 'GO_TO'
  | 'FILL_FIELD' | 'CLEAR_FIELD' | 'SUBMIT_FORM' | 'CANCEL_FORM'
  | 'SEARCH'
  | 'CREATE_ITEM' | 'EDIT_ITEM' | 'DELETE_ITEM'
  | 'NOOP';


export type APIResponse = {
  status: "success" | "error";
  message: string;
  action?: APIResult 
}

export type APIResult = { 
  command: string; 
  confidence: number;
  raw_text: string
}
