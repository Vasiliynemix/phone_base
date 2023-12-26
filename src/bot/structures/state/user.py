from aiogram.fsm.state import StatesGroup, State


class AddPhoneBaseState(StatesGroup):
    csv = State()
    name = State()
    text = State()
    end = State()


class EditPhoneBaseState(StatesGroup):
    text = State()
    file = State()


class GetLinksState(StatesGroup):
    quantity = State()
