from services import AIGameService
from core import GameStatus
from aiogram import types
from keyboards import GameKeyboard
from callbacks import GameCallback
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
        await message.answer(f"Игра с ботом запущена! Выберите столбец", reply_markup=self.game_keyboard.get_keyboard(game.board, message.from_user.id))

    async def game_callback_handler(self, callback_query: types.CallbackQuery, callback_data: GameCallback):
        first_player_id = callback_data.first_player_id
        user_id = callback_query.from_user.id
        print(user_id, "Нажал на", callback_data.col_index)
        column = callback_data.col_index
        if column == -1:
            await callback_query.answer("Выберите столбец", show_alert=True)
            return
        
        # Ход игрока
        result = self.ai_game_service.make_move(first_player_id, user_id, column)
        match result.status:
            case GameStatus.ONGOING:
                game = self.ai_game_service.games[first_player_id]
                print(game.render_board())
                active_player = self.ai_game_service.get_active_player(first_player_id)
                await callback_query.message.edit_text(
                    text=f"Ход: {active_player}",
                    reply_markup=self.game_keyboard.get_keyboard(game.board, callback_data.first_player_id)
                )
                
                # После хода игрока, бот делает свой ход
                await self.bot_turn(first_player_id, callback_query)

            case GameStatus.INVALID_MOVE:
                await callback_query.answer("Сейчас не ваш ход")
                return

            case GameStatus.WIN:
                winner = result.winner
                await callback_query.message.edit_text(
                    text=f"Победил {winner}",
                    reply_markup=None
                )
                return

            case GameStatus.DRAW:
                await callback_query.message.edit_text(
                    text="Ничья!",
                    reply_markup=None
                )
                return

    async def bot_turn(self, first_player_id: int, callback_query: types.CallbackQuery):
        """Метод, который делает ход бота после того, как игрок сделал свой ход."""
        await asyncio.sleep(2)  # Добавим задержку, чтобы бот "подумал"
        game = self.ai_game_service.games[first_player_id]
        bot_column = self.ai_game_service.ai.make_move(game.board)  # Бот делает ход

        if bot_column != -1:
            # Бот делает свой ход
            self.ai_game_service.make_move(first_player_id, first_player_id, bot_column)

            # Проверяем результат
            game = self.ai_game_service.games[first_player_id]
            if game.check_winner(bot_column, game.board[bot_column]):
                await callback_query.message.edit_text(
                    text="Победил бот!",
                    reply_markup=None
                )
                return

            if game.is_full():
                await callback_query.message.edit_text(
                    text="Ничья!",
                    reply_markup=None
                )
                return

            # Иначе продолжаем игру
            active_player = self.ai_game_service.get_active_player(first_player_id)
            await callback_query.message.edit_text(
                text=f"Ход: {active_player}",
                reply_markup=self.game_keyboard.get_keyboard(game.board, first_player_id)
            )
