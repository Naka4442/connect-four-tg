from services import AIGameService
from core import GameStatus
from aiogram import types
from keyboards import GameKeyboard
from callbacks import AIGameCallback
import asyncio


class AIGameHandler:
    def __init__(self, ai_game_service: AIGameService, game_keyboard: GameKeyboard):
        self.ai_game_service = ai_game_service
        self.game_keyboard = game_keyboard

    async def cmd_start_game_handler(self, message: types.Message):
        if not self.ai_game_service.start_game(message.from_user.id):
            await message.reply("Для вас игра уже где-то запущена! Используйте /restart для перезапуска игры")
            return
        game = self.ai_game_service.games[message.from_user.id]
        await message.answer(
            text="Игра с ботом запущена! Выберите столбец",
            reply_markup=self.game_keyboard.get_ai_keyboard(game.board)
        )

    async def game_callback_handler(self, callback_query: types.CallbackQuery, callback_data: AIGameCallback):
        user_id = callback_query.from_user.id
        column = callback_data.col_index

        if column == -1:
            await callback_query.answer("Выберите столбец", show_alert=True)
            return

        # Ход игрока
        result = self.ai_game_service.make_move(user_id, column)
        game = self.ai_game_service.games.get(user_id)

        match result.status:
            case GameStatus.INVALID_MOVE:
                await callback_query.answer("Неверный ход! Попробуйте другой столбец.")
                return

            case GameStatus.WIN:
                await callback_query.message.edit_text(f"Победил {result.winner}!", reply_markup=None)
                return

            case GameStatus.DRAW:
                await callback_query.message.edit_text("Ничья!", reply_markup=None)
                return

        # Обновляем доску после хода игрока
        await callback_query.message.edit_text(
            text=f"Ход: {self.ai_game_service.get_active_player(user_id)}",
            reply_markup=self.game_keyboard.get_ai_keyboard(game.board)
        )

        # Ход бота
        await asyncio.sleep(1)
        bot_result = self.ai_game_service.bot_move(user_id)

        # Проверяем результат хода бота
        match bot_result.status:
            case GameStatus.WIN:
                await callback_query.message.edit_text("Победил бот!", reply_markup=None)
                return

            case GameStatus.DRAW:
                await callback_query.message.edit_text("Ничья!", reply_markup=None)
                return

        # Обновляем доску после хода бота
        await callback_query.message.edit_text(
            text=f"Ход: {self.ai_game_service.get_active_player(user_id)}",
            reply_markup=self.game_keyboard.get_ai_keyboard(game.board)
        )
