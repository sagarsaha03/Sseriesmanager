from aiogram.utils.keyboard import InlineKeyboardBuilder

def help_keyboard(page=0):
    commands = [
        ("/start", "Start bot"),
        ("/status", "Check bot status"),
        ("/set_channel", "Configure channels"),
        ("/list_channels", "List all channels"),
        ("/set_config", "Change bot settings"),
        ("/reload", "Reload configuration"),
        ("/duplicates", "List pending duplicates"),
    ]
    
    builder = InlineKeyboardBuilder()
    
    # Pagination logic (5 commands per page)
    start = page * 5
    end = min(start + 5, len(commands))
    
    for cmd, desc in commands[start:end]:
        builder.button(text=desc, callback_data=f"help_{cmd[1:]}")
    
    # Navigation buttons
    if page > 0:
        builder.button(text="⬅️ Previous", callback_data=f"help_page_{page-1}")
    if end < len(commands):
        builder.button(text="Next ➡️", callback_data=f"help_page_{page+1}")
    
    builder.adjust(1, 2)
    return builder.as_markup()

def duplicate_keyboard(original_id, duplicate_id):
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Keep Both", callback_data=f"dup_keep_{original_id}_{duplicate_id}")
    builder.button(text="🗑️ Delete Duplicate", callback_data=f"dup_del_{duplicate_id}")
    builder.button(text="⏹️ Delete Original", callback_data=f"dup_del_{original_id}")
    builder.adjust(1, 2)
    return builder.as_markup()
