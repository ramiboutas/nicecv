class Form:
    class TextInput:
        html_class = "border-1 rounded-md hover:bg-indigo-100 border-indigo-100"
        x_bind_class = "active ? 'border-indigo-400' : 'border-indigo-100'"
        hx_trigger = "keyup changed delay:2s, change"

    class CheckBox:
        html_class = "h-4 w-4 rounded border-indigo-400 focus:ring-indigo-400"
