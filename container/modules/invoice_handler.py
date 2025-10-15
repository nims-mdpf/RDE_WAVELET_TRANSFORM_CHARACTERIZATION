from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from rdetoolkit.invoicefile import InvoiceFile, overwrite_invoicefile_for_dpfterm
from rdetoolkit.models.rde2types import RdeOutputResourcePath
from rdetoolkit.rde2util import read_from_json_file


class InvoiceWriter:
    """Invoice overwriter.

    Overwrite invoice.json files depending on conditions.

    """

    def overwrite_invoice_calculated_date(
        self,
        resource_paths: RdeOutputResourcePath,
    ) -> None:
        """Overwrite invoice if needed.

        The date is to be obtained from the output device and output to invoice.
        The measurement date and time are written automatically to the invoice.json file
        # based on the file meta data output from the device, so I added a process to write it to invoice.json.

        Args:
            suffix (str): Input file extension.
            resource_paths (RdeOutputResourcePath): Paths to output resources for saving results.
            meta: (dict[str, ExtendMetaType]): Metadata.

        """
        """Overwrite the calculated date information in an invoice JSON file.

        This method reads an original invoice JSON file, determines whether the
        calculation‑date metadata has to be updated, and if so overwrites the
        invoice file with the updated metadata.  After the overwrite the
        resulting invoice file is copied to ``resource_paths.invoice/invoice.json``.

        Args:
            resource_paths (RdeOutputResourcePath): An object that provides the
                following path attributes:
                - ``invoice_org``: Path to the original invoice JSON file.
                - ``invoice_schema_json``: Path to the JSON schema used for
                validation.
                - ``invoice``: Directory path where the final invoice JSON will be
                stored.

        Returns:
            None

        Raises:
            FileNotFoundError: If ``resource_paths.invoice_org`` does not exist.
            json.JSONDecodeError: If the original invoice file cannot be parsed as
                JSON.
            SomeCustomError: Propagated from ``_get_update_calculation_date_dpf_metadata``
                or ``overwrite_invoicefile_for_dpfterm`` when the update process fails.
        """
        invoice_obj = read_from_json_file(resource_paths.invoice_org)
        update_invoice_term_info = self._get_update_calculation_date_dpf_metadata(
            invoice_obj,
        )
        if update_invoice_term_info:
            overwrite_invoicefile_for_dpfterm(
                invoice_obj,
                resource_paths.invoice_org,
                resource_paths.invoice_schema_json,
                update_invoice_term_info,
            )
            invoice_org_obj = InvoiceFile(resource_paths.invoice_org)
            invoice_org_obj.overwrite(resource_paths.invoice.joinpath("invoice.json"))

    def _get_update_calculation_date_dpf_metadata(
        self,
        invoice_obj: dict[str, Any],
    ) -> dict[str, str]:
        """Extract and possibly generate a calculation date for a DPF invoice.

        This helper inspects the ``custom`` section of ``invoice_obj`` and
        returns a dictionary that contains the key ``"calculation_calculated_date"``.
        If the key is missing, an empty dictionary is returned.  When the key exists
        but its value is ``None``, the current date (in ``YYYY‑MM‑DD`` format) is
        used as a fallback.

        Args:
            invoice_obj: A dictionary that represents an invoice.  It must contain
                a ``"custom"`` key whose value is a mapping.  The mapping may hold
                the ``"calculation_calculated_date"`` entry whose value is either a
                string in ``YYYY‑MM‑DD`` format or ``None``.

        Returns:
            dict: A dictionary with a single entry
            ``{"calculation_calculated_date": <date_str>}`` when the
            ``calculation_calculated_date`` field is present (or generated), or an
            empty dictionary when the field is absent.

        """
        update_invoice_term_info: dict[str, str] = {}
        if "calculation_calculated_date" not in invoice_obj["custom"]:
            return update_invoice_term_info
        calculated_date: str | None = invoice_obj["custom"].get("calculation_calculated_date")
        if calculated_date is None:
            tdate = datetime.now(timezone.utc)
            calculated_date = f"{tdate.year:04d}-{tdate.month:02d}-{tdate.day:02d}"
        update_invoice_term_info["calculation_calculated_date"] = calculated_date
        return update_invoice_term_info
