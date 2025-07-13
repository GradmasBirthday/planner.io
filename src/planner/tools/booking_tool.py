import asyncio
import os
from typing import Type, Optional, Dict, Any

from crewai import BaseTool
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from stagehand import Stagehand
from stagehand.schemas import ExtractOptions

# Load environment variables
load_dotenv()

# --- Pydantic Schemas ---

class BookingPreview(BaseModel):
    """Data schema for the extracted booking preview."""
    name: Optional[str] = None
    email: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    guests: Optional[int] = None


class BookingToolInput(BaseModel):
    """Input schema for booking tools."""
    form_url: str = Field(..., description="The URL of the booking form to be filled.")
    data: Dict[str, Any] = Field(..., description="A dictionary of data to fill the form with. Keys should be the field names.")


# --- Helper Functions (internal to the tool) ---

async def _fill_form_on_page(page, data: dict):
    """Fills the form on the given page with the provided data."""
    for field, value in data.items():
        try:
            label = field.replace('_', ' ').capitalize()
            await page.act(f"Type '{value}' into the input field labeled '{label}'")
            print(f"Successfully filled '{label}' field.")
        except Exception:
            print(f"Could not find or fill field for '{label}'. Skipping.")


# --- CrewAI Tools ---

class PreviewBookingTool(BaseTool):
    name: str = "Preview Booking Form"
    description: str = "Fills out a booking form with provided data and returns a JSON preview of the filled information. Use this to verify form contents before submission."
    args_schema: Type[BaseModel] = BookingToolInput

    def _run(self, form_url: str, data: Dict[str, Any]) -> str:
        return asyncio.run(self._arun(form_url=form_url, data=data))

    async def _arun(self, form_url: str, data: Dict[str, Any]) -> str:
        """Asynchronously fills the form and returns a preview."""
        sh = None
        try:
            sh = Stagehand(
                browserbase_api_key=os.getenv("BROWSERBASE_API_KEY"),
                browserbase_project_id=os.getenv("BROWSERBASE_PROJECT_ID"),
                model_api_key=os.getenv("OPENAI_API_KEY"),
                model_name="openai/gpt-4"
            )
            await sh.init()
            p = sh.page
            await p.goto(form_url)
            await _fill_form_on_page(p, data)

            preview = await p.extract(
                ExtractOptions(
                    instruction="Extract the filled booking preview fields. If a field is not present, ignore it.",
                    schemaDefinition=BookingPreview
                )
            )
            return preview.json()
        finally:
            if sh:
                await sh.close()


class SubmitBookingTool(BaseTool):
    name: str = "Submit Booking Form"
    description: str = "Fills out a booking form with provided data and clicks the submit button to finalize the booking."
    args_schema: Type[BaseModel] = BookingToolInput

    def _run(self, form_url: str, data: Dict[str, Any]) -> str:
        return asyncio.run(self._arun(form_url=form_url, data=data))

    async def _arun(self, form_url: str, data: Dict[str, Any]) -> str:
        """Asynchronously fills and submits the form."""
        sh = None
        try:
            sh = Stagehand(
                browserbase_api_key=os.getenv("BROWSERBASE_API_KEY"),
                browserbase_project_id=os.getenv("BROWSERBASE_PROJECT_ID"),
                model_api_key=os.getenv("OPENAI_API_KEY"),
                model_name="openai/gpt-3.5-turbo"
            )
            await sh.init()
            p = sh.page
            await p.goto(form_url)
            await _fill_form_on_page(p, data)

            await p.act("click the submit button")
            await p.act("wait for confirmation message or page")
            return "Booking submitted successfully."
        finally:
            if sh:
                await sh.close() 