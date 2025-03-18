from services import GameService, GameStatus
from aiogram import types
from keyboards import GameKeyboard
from callbacks import GameCallback


class GameHandler:
    def __init__(self, game_service: GameService, game_keyboard: GameKeyboard):
        self.game_service = game_service
        self.game_keyboard = game_keyboard
        
    async def cmd_start_game_handler(self, message: types.Message):
        if not self.game_service.start_game(message.from_user.id):
            await message.reply("Игра уже запущена! Используйте /join_game.")
            return
        game = self.game_service.games[message.from_user.id]
        await message.answer(f"Игра запущена! Выберите столбец", reply_markup=self.game_keyboard.get_keyboard(game.board, message.from_user.id))

    async def game_callback_handler(self, callback_query: types.CallbackQuery, callback_data: GameCallback):
        first_player_id = callback_data.first_player_id
        user_id = callback_query.from_user.id
        print(user_id, "Нажал на", callback_data.col_index)
        column = callback_data.col_index
        if column == -1:
            await callback_query.answer("Выберите столбец", show_alert=True)
            return
        result = self.game_service.make_move(first_player_id, user_id, column)
        match result.status:
            case GameStatus.ONGOING:
                game = self.game_service.games[first_player_id]
                print(game.render_board())
                active_player = self.game_service.get_active_player(first_player_id)
                await callback_query.message.edit_text(
                    text=f"Ход: {active_player}", 
                    reply_markup=self.game_keyboard.get_keyboard(game.board, callback_data.first_player_id)
                )
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