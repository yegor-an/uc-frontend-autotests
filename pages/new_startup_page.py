from selene import browser
from config import BASE_URL


class NewStartupPage:
    NAME_INPUT = '#startupName'
    AVATAR_BUTTON = '#startupAvatar'
    AVATAR_REMOVE_BUTTON = '#remove-button'
    CEO_NAME_INPUT = '#ceoName'
    CEO_LINKEDIN_INPUT = '#seoLinkedin'
    CEO_PHOTO_BUTTON = '#seoPhoto'
    CEO_PHOTO_REMOVE_BUTTON = '#remove-button'
    MAIN_INDUSTRY_INPUT = '#mainIndustry'
    RELEVANT_INDUSTRIES_INPUT = '#relevantIndustries'
    WEBSITE_INPUT = '#startupWebsite'
    NO_WEBSITE_CHECKBOX = '#noWebsite'
    HEADQUARTERS_INPUT = '#country_registration'
    FOUNDERS_BASED_INPUT = '#team_location'
    BACKGROUND_INPUT = '#team_location'
