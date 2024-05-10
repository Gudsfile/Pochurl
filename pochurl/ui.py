import logging
from functools import cache
from typing import Annotated, List

from fastapi import APIRouter, HTTPException
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import BackEvent, GoToEvent, PageEvent
from fastui.forms import fastui_form

from pochurl import api
from pochurl.core import get_db
from pochurl.domain import GivenElement, GivenElementForm, SavedElement, TagFilterForm


logger = logging.getLogger(__name__)
db = get_db('tinydb')
router = APIRouter(
    prefix='/ui',
    tags=['ui'],
    include_in_schema=False,
)


PAGE_EVENT_TO_ADD = 'modal-form-add'
PAGE_EVENT_ADDED = 'show-toast-added'


@cache
def elements_list():
    return api.get_items(db)


@router.get('/', response_model=FastUI, response_model_exclude_none=True)
def show_items(page: int = 1, tag: str | None = None) -> List[AnyComponent]:
    elements = elements_list()
    page_size = 10
    filter_form_initial = {}
    if tag:
        elements = [element for element in elements if tag in element.tags]
        filter_form_initial['tag'] = {'value': tag, 'label': tag}
    return [
        c.Page(
            components=[
                c.Heading(text='Urls', level=2),

                c.Button(text='Add an element', on_click=PageEvent(name=PAGE_EVENT_TO_ADD)),
                c.Button(text='Refresh elements', on_click=GoToEvent(url='/refresh')),
                c.Modal(
                    title='Add an element',
                    body=[c.ModelForm(model=GivenElementForm, display_mode='page', submit_url='/ui/element')],
                    open_trigger=PageEvent(name=PAGE_EVENT_TO_ADD),
                ),
                c.Toast(
                    title='Success',
                    body=[
                        c.Paragraph(text='The item has been added successfully !'),
                        c.Paragraph(text='Press "refresh" to view it in the list.')
                    ],
                    open_trigger=PageEvent(name=PAGE_EVENT_ADDED),
                    position='bottom-end',
                ),

                c.ModelForm(
                    model=TagFilterForm,
                    submit_url='.',
                    initial=filter_form_initial,
                    method='GOTO',
                    submit_on_change=True,
                    display_mode='inline',
                ),

                c.Table(
                    data=elements[(page - 1) * page_size : page * page_size],
                    data_model=SavedElement,
                    columns=[
                        DisplayLookup(field='id', on_click=GoToEvent(url='/element/{id}')),
                        DisplayLookup(field='name'),
                        DisplayLookup(field='url', on_click=GoToEvent(url='{url}')),
                        DisplayLookup(field='tags'),
                        DisplayLookup(field='timestamp', title='Date added', mode=DisplayMode.datetime),
                    ],
                ),
                c.Pagination(page=page, page_size=page_size, total=len(elements)),
            ]
        ),
    ]


@router.get('/element/{id}', response_model=FastUI, response_model_exclude_none=True)
def show_item(id: str) -> list[AnyComponent]:
    element = api.get_item(id, db)
    if element is None:
        raise HTTPException(status_code=404, detail='Element not found')
    return [
        c.Page(
            components=[
                c.Heading(text=element.name, level=2),
                c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),
                c.Details(data=element),
                c.Iframe(src=element.url, width='100%', height=400),
            ]
        ),
    ]


@router.get('/refresh', response_model=FastUI, response_model_exclude_none=True)
def refresh_items() -> List[AnyComponent]:
    elements_list.cache_clear()
    return [c.FireEvent(event=BackEvent())]


@router.post('/element', response_model=FastUI, response_model_exclude_none=True)
def add_item(form: Annotated[GivenElementForm, fastui_form(GivenElementForm)]) -> list[AnyComponent]:
    element = GivenElement(url=form.url, name=form.name, tags=set(form.tag) if form.tag else set())
    api.add_item(element, db)
    return [c.FireEvent(event=PageEvent(name=PAGE_EVENT_TO_ADD, clear=True)), c.FireEvent(event=PageEvent(name=PAGE_EVENT_ADDED))]
