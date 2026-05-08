import httpx


async def validate_artwork(external_id: int):
    url = f"https://api.artic.edu/api/v1/artworks/{external_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    return response.status_code == 200