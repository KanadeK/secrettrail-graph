from leakloom.domain.privacy import fingerprint, mask


def test_fingerprint_is_stable_and_irreversible() -> None:
    secret = "LLM_FAKE_ALPHA_7a9K2mP4qR8x"
    assert fingerprint(secret) == fingerprint(secret)
    assert secret not in fingerprint(secret)


def test_mask_hides_middle() -> None:
    secret = "LLM_FAKE_ALPHA_7a9K2mP4qR8x"
    assert mask(secret).startswith("LLM")
    assert mask(secret).endswith("R8x")
    assert secret not in mask(secret)
